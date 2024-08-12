import mariadb
import sys, datetime

conn = mariadb.connect(
        # insert your DB INFO
        user="",
        password="",
        host="",
        port=3306,
        database=""
)
def getName(ID):
        cursor = conn.cursor()
        sql = 'select * from users'
        cursor.execute(sql)
        result = cursor.fetchall()
        for id, pswd, name, birth, gender, email in result:
                if id == ID:
                        return name
#회원가입
def registerUser(ID, PSWD, NAME, BIRTH, GENDER, EMAIL):
        cursor = conn.cursor()
        sql = 'select * from users'
        cursor.execute(sql)
        result = cursor.fetchall()
        for id, pswd, name, birth, gender, email in result:
                if id == ID:
                        return False
        sql = "INSERT INTO users(id, pswd, name, birth, gender, email) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (ID, PSWD, NAME, BIRTH, GENDER, EMAIL)
        cursor.execute(sql, values)
        conn.commit()
        return True
#로그인체크
def logincheck(ID, PSWD):
        cursor = conn.cursor()
        sql = 'select * from users'
        cursor.execute(sql)
        result = cursor.fetchall()
        for id, pswd, name, birth, gender, email in result:
                if id == ID and pswd == PSWD:
                        return True
        return False
#선호도추가
def addpreference(ID, FD_PREF):
    cursor = conn.cursor()
    
    # 사용자의 기존 선호도 조회
    select_sql = "SELECT * FROM preference WHERE id = %s"
    cursor.execute(select_sql, (ID,))
    result = cursor.fetchone()
    
    # 기존 선호도가 없는 경우 새로 추가
    if not result:
        insert_sql = "INSERT INTO preference (id, fd_preference) VALUES (%s, %s)"
        cursor.execute(insert_sql, (ID, FD_PREF))
    else:
        # 기존 선호도가 있는 경우 업데이트
        update_sql = "UPDATE preference SET fd_preference = %s WHERE id = %s"
        cursor.execute(update_sql, (FD_PREF, ID))
    
    conn.commit()

 #알러지추가
def addallergy(ID, ALLERGY):
        cursor = conn.cursor()
        sql = 'select * from allergy'
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:    # result가 비어있는 경우
                sql = "INSERT INTO allergy(id, allergy) VALUES (%s, %s)"
                values = (ID, ALLERGY)
                cursor.execute(sql, values)
        else:
                for id, allergy in result:
                        if id == ID:    #아이디가 있으면 이미 입력이 된것이므로 update
                                sql = "UPDATE allergy SET allergy = %s WHERE id = %s"
                                values = (ALLERGY, ID)
                                cursor.execute(sql, values)
                                conn.commit()
                                return
                #아이디가 없으면 처음 데이터를 입력
                sql = "INSERT INTO allergy(id, allergy) VALUES (%s, %s)"
                values = (ID, ALLERGY)
                cursor.execute(sql, values)
                conn.commit()      

def search_data(userid):
        cursor = conn.cursor()
        sql = ("SELECT fd_preference FROM preference WHERE id = %s")
        value = (userid,)
        cursor.execute(sql, value)
        results = cursor.fetchall()

        food_ingredients_search_sql = ("SELECT fd_ingredients FROM food")
        cursor.execute(food_ingredients_search_sql)
        food_ingredients = cursor.fetchall()

        food_name_search_sql = ("SELECT fd_name FROM food")
        cursor.execute(food_name_search_sql)
        food_name = cursor.fetchall()
        food_names = [row[0] for row in food_name]

        return results, food_ingredients, food_names

def add_food(userid, food_name):
    cursor = conn.cursor()
    # 현재 날짜 가져오기
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 음식 코드 가져오기
    select_fd_code_sql = "SELECT fd_code FROM food WHERE fd_name = %s"
    cursor.execute(select_fd_code_sql, (food_name,))
    fd_code_result = cursor.fetchone()
    fd_code = fd_code_result[0] if fd_code_result else None
    
    if not fd_code:
        # fd_code가 없으면 종료
        return "Food not found"
    
    # 음식 영양 정보 가져오기
    select_nutrients_sql = "SELECT energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot FROM food_nutrients WHERE fd_code = %s"
    cursor.execute(select_nutrients_sql, (fd_code,))
    nutrient_result = cursor.fetchone()
    
    if nutrient_result:
        energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot = nutrient_result
    else:
        # 영양 정보가 없는 경우 기본값 설정
        energy = na = cbh = sugar = fat = transfat = saturatedfat = kol = prot = 0

    # 새로운 레코드 삽입
    insert_sql = "INSERT INTO list (userid, intakedt, fd_code, fd_name, energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_sql, (userid, current_date, fd_code, food_name, energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot))

    conn.commit()
    
def reset_food(userid):
    cursor = conn.cursor()
    delete_sql = "DELETE FROM list WHERE userid = %s"
    cursor.execute(delete_sql, (userid,))
    conn.commit()

def get_food_list(userid):
        cursor = conn.cursor()
        select_sql = "SELECT fd_name FROM list WHERE userid = %s"
        cursor.execute(select_sql, (userid,))
        result = cursor.fetchall()
        food_list = [row[0] for row in result] if result else []
        return food_list

def get_nutrient_list(userid):
    cursor = conn.cursor()
    select_sql = "SELECT energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot FROM list WHERE userid = %s"
    cursor.execute(select_sql, (userid,))
    results = cursor.fetchall()

    if not results:
        print("섭취한 식단이 없습니다.")
        return None
    else:
        nutrient_totals = {
            'energy': 0.0,
            'na': 0.0,
            'cbh': 0.0,
            'sugar': 0.0,
            'fat': 0.0,
            'transfat': 0.0,
            'saturatedfat': 0.0,
            'kol': 0.0,
            'prot': 0.0
        }

        for result in results:
            energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot = result
            nutrient_totals['energy'] += round(energy, 1)
            nutrient_totals['na'] += round(na, 1)
            nutrient_totals['cbh'] += round(cbh, 1)
            nutrient_totals['sugar'] += round(sugar, 1)
            nutrient_totals['fat'] += round(fat, 1)
            nutrient_totals['transfat'] += round(transfat, 1)
            nutrient_totals['saturatedfat'] += round(saturatedfat, 1)
            nutrient_totals['kol'] += round(kol, 1)
            nutrient_totals['prot'] += round(prot, 1)

        nutrient_values = list(nutrient_totals.values())
        return nutrient_values



def get_user_info(userid):
    cursor = conn.cursor()
    select_sql = "SELECT birth, gender FROM users WHERE id = %s"
    cursor.execute(select_sql, (userid,))
    result = cursor.fetchone()
    if result:
        birth_date = result[0]
        gender = result[1]
        return birth_date, gender
    else:
        return None, None


def get_user_all_info(userid):
    cursor = conn.cursor()
    select_sql = "SELECT id, pswd, name, birth, gender FROM users WHERE id = %s"
    cursor.execute(select_sql, (userid,))
    result = cursor.fetchone()
    if result:
        id= result[0]
        pswd= result[1]
        name= result[2]
        birth= result[3]
        gender= result[4]
        return id, pswd, name, birth, gender
    else:
        return None

