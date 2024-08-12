import base64  # 이진 데이털르 텍스트로 변환

import requests
from flask import Flask, redirect, render_template, request, session, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
import cos, ocr
import database.mariaDB as mariaDB
import os
from cos import *
from database.mariaDB import conn

app = Flask(__name__)
app.secret_key = "seknjfsnkljgsdf"

UPLOAD_FOLDER = 'static/ocr_image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def getname():
    username = mariaDB.getName(session.get("userID"))
    return username

@app.route('/')
def index():
    if "userID" in session:
        return render_template("home.html",username = getname(), login = True)
    else:
        return render_template("home.html")

@app.route('/login')
def login():
    log_fail = request.args.get("log_fail")
    if log_fail:
        return render_template('top_menu/login.html', log=True)
    else:
        return render_template('top_menu/login.html')

@app.route("/logout")
def logout():
    session.pop("userID")
    return redirect(url_for("index"))

@app.route('/login_check', methods = ["get"])
def login_check():
    _id_ = request.args.get("username")
    _password_ = request.args.get("password")
    login = mariaDB.logincheck(_id_, _password_)

    if login==True :
        session["userID"] = _id_
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login", log_fail = True))

@app.route('/sign_up')
def sign_up():
    pswddiff = request.args.get("pswddiff")
    duplicate = request.args.get("duplicate")
    if pswddiff:
        return render_template("top_menu/sign_up.html", diff=True)
    elif duplicate:
        return render_template("top_menu/sign_up.html", dup=True)
    else:
        return render_template('top_menu/sign_up.html')

@app.route("/register_done", methods = ["get"])
def register_done():
    _id_ = request.args.get("userid")
    _password_ = request.args.get("password")
    _confirm_pswd_ = request.args.get("confirm_password")
    _name_ = request.args.get("name")

    _yy_ = request.args.get("yy")
    _mm_ = request.args.get("mm")
    _dd_ = request.args.get("dd")

    _mm_ = '0' + _mm_ if len(_mm_) == 1 else _mm_
    _dd_ = '0' + _dd_ if len(_dd_) == 1 else _dd_
    _birth_ = _yy_ + _mm_ + _dd_
    #_birth_ = request.args.get("yy"+"mm"+"dd")
    _gender_ = request.args.get("gender")
    
    #_email1 = request.args.get("email1")
    #_email2 = request.args.get("email2")
    #_email_ = _email1 + "@" + _email2
    _email_ = request.args.get("email")

    idcheck = mariaDB.registerUser(_id_, _password_, _name_, _birth_, _gender_, _email_)
    if idcheck == True:
        if _password_ == _confirm_pswd_:
            return redirect(url_for("index"))
        else:       #패스워드 불일치
            return redirect(url_for("sign_up", pswddiff = True))
    else:   #아이디 중복
        return redirect(url_for("sign_up",duplicate = True))

@app.route('/submit_preference')
def submit_preference():
    if "userID" in session:
        return render_template("top_menu/submit_preference.html",username = getname(), login = True)
    else:
        return render_template('top_menu/submit_preference.html')
    
@app.route('/submit_preference_done', methods=['GET'])
def submit_preference_done():
    selected_allergies = request.args.getlist('allergy[]')
    selected_allergies_str = ', '.join(selected_allergies)
    print(selected_allergies_str)
    mariaDB.addallergy(session.get("userID"), selected_allergies_str)

    selected_preferences = request.args.getlist('preferences[]')
    selected_preferences_str = ', '.join(selected_preferences)
    print(selected_preferences_str)
    mariaDB.addpreference(session.get("userID"), selected_preferences_str)
    return redirect(url_for("my_info"))

@app.route('/my_info.html')
def my_info():
    if "userID" in session:
        id, pswd, name, birth, gender = mariaDB.get_user_all_info(session.get("userID"))
        birth = birth[:4] + '.' + birth[4:6] + '.' + birth[6:]
        return render_template('top_menu/my_info.html',username = getname(), id=id, pswd=pswd, name=name, birth=birth, gender=gender, login=True)
    else:
        return render_template('top_menu/my_info.html')

@app.route('/menu_recommendations')
def menu_recommendations():
    if "userID" in session:
        result, food_ingredients, food_name = mariaDB.search_data(session.get("userID"))
        preference_food_list=cos.check_preference(result, food_ingredients, food_name)
        return render_template('main_category/menu_recommendations.html',preference_food = preference_food_list, username = getname(), login = True)
    else:
        return render_template('main_category/menu_recommendations.html')
    
@app.route('/add_food_list/<food_name>')
def add_food_list(food_name):
    mariaDB.add_food(session.get("userID"), food_name)
    return redirect(url_for("menu_recommendations"))

@app.route('/reset_food_list')
def reset_food_list():
    mariaDB.reset_food(session.get("userID"))
    return redirect(url_for("menu_recommendations"))
    
@app.route('/intake_menu')
def intake_menu():
    if "userID" in session:
        food_list=mariaDB.get_food_list(session.get("userID"))
        print(food_list)
        return render_template('main_category/intake_menu.html',food_list = food_list, username = getname(), login = True)
    else:
        return render_template('main_category/intake_menu.html')  
        
@app.route('/nutrient_intake')
def nutrient_intake():
    if "userID" in session:
        nutrient_list = mariaDB.get_nutrient_list(session.get("userID"))
        _birth_, _gender_ = mariaDB.get_user_info(session.get("userID"))

        birth_date = datetime.strptime(_birth_, "%Y%m%d")
        current_date = datetime.now()
        age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
        recommended_intake = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # 출처: 보건복지부 2020 한국인 영양소 섭취기준 활용.pdf
        if _gender_ == "male":
            if age >= 1 and age <= 2:
                recommended_intake = [950, 1000, 130, 25, 30, 1, 10, 300, 20]
            elif age >= 3 and age <= 5:
                recommended_intake = [1400, 1200, 180, 30, 40, 1, 15, 300, 25]
            elif age >= 6 and age <= 8:
                recommended_intake = [1600, 1500, 220, 35, 50, 1, 18, 300, 30]
            elif age >= 9 and age <= 11:
                recommended_intake = [1900, 1800, 260, 40, 55, 1, 20, 300, 35]
            elif age >= 12 and age <= 14:
                recommended_intake = [2400, 2000, 300, 45, 65, 1, 22, 300, 40]
            elif age >= 15 and age <= 18:
                recommended_intake = [2800, 2300, 340, 50, 70, 1, 24, 300, 45]
            elif age >= 19 and age <= 29:
                recommended_intake = [2700, 2500, 360, 55, 75, 1, 25, 300, 50]
            elif age >= 30 and age <= 49:
                recommended_intake = [2600, 2500, 360, 55, 75, 1, 25, 300, 50]
            elif age >= 50 and age <= 64:
                recommended_intake = [2400, 2300, 340, 50, 70, 1, 24, 300, 45]
            elif age >= 65:
                recommended_intake = [2200, 2100, 320, 45, 65, 1, 22, 300, 40]
        elif _gender_ == "female":
            if age >= 1 and age <= 2:
                recommended_intake = [900, 1000, 120, 20, 28, 1, 10, 300, 18]
            elif age >= 3 and age <= 5:
                recommended_intake = [1300, 1200, 160, 25, 35, 1, 15, 300, 22]
            elif age >= 6 and age <= 8:
                recommended_intake = [1500, 1500, 200, 30, 45, 1, 18, 300, 26]
            elif age >= 9 and age <= 11:
                recommended_intake = [1800, 1800, 240, 35, 50, 1, 20, 300, 30]
            elif age >= 12 and age <= 14:
                recommended_intake = [2200, 2000, 280, 40, 60, 1, 22, 300, 34]
            elif age >= 15 and age <= 18:
                recommended_intake = [2400, 2300, 320, 45, 65, 1, 24, 300, 38]
            elif age >= 19 and age <= 29:
                recommended_intake = [2200, 2500, 340, 50, 70, 1, 25, 300, 40]
            elif age >= 30 and age <= 49:
                recommended_intake = [2100, 2500, 340, 50, 70, 1, 25, 300, 40]
            elif age >= 50 and age <= 64:
                recommended_intake = [2000, 2300, 320, 45, 65, 1, 24, 300, 38]
            elif age >= 65:
                recommended_intake = [1800, 2100, 300, 40, 60, 1, 22, 300, 34]

        print(nutrient_list)
        print(recommended_intake)
        if nutrient_list:
            nutrient_percentages = [round((nutrient / recommended) * 100, 1) if recommended != 0 and nutrient != 0 else 0 for nutrient, recommended in zip(nutrient_list, recommended_intake)]
            return render_template('main_category/nutrient_intake.html', nutrient_list=nutrient_percentages, username=getname(), login=True)
        else:
            return render_template('main_category/nutrient_intake.html', username=getname(), login=True)
    else:
        return render_template('main_category/nutrient_intake.html')
  
@app.route('/nutrition_facts')
def nutrition_facts():
    file_path = request.args.get('file_path', None)
    print("file_path :", file_path)
    if file_path: # file_path가 있을 때 OCR 분석 수행
        energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot, cautions = ocr.analyze_ocr(file_path)
        if "userID" in session:
            return render_template('main_category/nutrition_facts.html', 
                                energy=energy, na=na, cbh=cbh, sugar=sugar, 
                                fat=fat, transfat=transfat, saturatedfat=saturatedfat, 
                                kol=kol, prot=prot, cautions=cautions, 
                                username=getname(), login=True, file_path=file_path.replace('\\', '/'))
        else:
            return render_template('main_category/nutrition_facts.html', 
                                energy=energy, na=na, cbh=cbh, sugar=sugar, 
                                fat=fat, transfat=transfat, saturatedfat=saturatedfat, 
                                kol=kol, prot=prot, cautions=cautions, file_path=file_path.replace('\\', '/'))
    else: # file_path가 없을 때 기본 템플릿 렌더링
        if "userID" in session:
            return render_template('main_category/nutrition_facts.html',username=getname(), login=True)
        else:
            return render_template('main_category/nutrition_facts.html')
    
def nutrition_facts():
    if "userID" in session:
        energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot, cautions = ocr.analyze_ocr('static/ocr_image/test.jpg')
        return render_template('main_category/nutrition_facts.html',energy=energy, na=na, cbh=cbh, sugar=sugar, fat=fat, transfat=transfat, saturatedfat=saturatedfat, kol=kol, prot=prot, cautions=cautions, username = getname(), login = True)
    else:
        return render_template('main_category/nutrition_facts.html')
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_done', methods=['POST'])
def upload_done():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # 업로드된 파일의 경로를 템플릿에 전달
        return redirect(url_for('nutrition_facts', file_path=file_path))
    return 'File not allowed'

@app.route('/save_food_db', methods=['get'])
def save_food_db():
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
