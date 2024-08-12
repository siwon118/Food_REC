import requests
import uuid
import time
import json
def extraction(string, keyword) :
    lst = []
    for i in range(len(string)):
        if keyword in string[i]:
            if i > 0 and keyword == 'kcal' : lst.append(string[i-1])
            lst.append(string[i])
            if i < len(string)-1 : lst.append(string[i+1])
    for i in range(len(lst)):
        lst[i] = lst[i].replace(",","")
        lst[i] = lst[i].replace(keyword,"")
        lst[i] = lst[i].replace("mg","")
        lst[i] = lst[i].replace("g","")
        if is_num(lst[i]) :
            return float(lst[i])
    return 0

def is_num(string) :
    for i in range(len(string)) :
        if not string[i].isdigit() and string[i] != '.' :
            return False
        return True

def analyze_ocr(image_path):
    api_url = 'https://hrksxbmwcd.apigw.ntruss.com/custom/v1/30071/9605970d2db830c95f3b3706dbc6fd8df47bcdbb0f43c096830176b5eb6baa33/general'
    secret_key = 'VmNpYm1pUE9sZFNlZ3pha3VLYUhCV1hpYmFka2RrVWo='
    image_file = image_path

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
    ('file', open(image_file,'rb'))
    ]
    headers = {
    'X-OCR-SECRET': secret_key
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    s1 = []
    s2 = ""
    allergy = ['계란', '우유', '밀', '갑각류', '생선', '호두', '돼지고기', '땅콩', '조개', '복숭아']
    state = 0
    for i in response.json()['images'][0]['fields']:
        text = i['inferText']
        s2+=text
        s1.append(text)
    allergy = ['계란', '우유', '밀', '게', '새우', '생선', '호두', '돼지고기', '땅콩', '조개', '복숭아']
    cautions = []
    함유 = 0
    for i in range(len(s1)) :
        if s1[i].replace(",","") == "함유" :
            print(i, s1[i]);
            함유 = i

    for i in range(함유-30,함유) :
        for j in range(len(allergy)) :
            if s1[i].replace(",","") == allergy[j] :
                cautions.append(allergy[j])
    print("알레르기", str(cautions))
    # 영양정보
    energy = extraction(s1,'kcal') # 열량
    na = extraction(s1,'나트륨') # 나트륨
    cbh = extraction(s1,'탄수화물') # 탄수화물
    sugar = extraction(s1, '당류') # 당류
    fat = extraction(s1, '지방') # 지방
    transfat = extraction(s1, '트랜스지방') # 트랜스 지방
    saturatedfat = extraction(s1, '포화지방') # 포화 지방
    kol = extraction(s1,'콜레스테롤') # 콜레스테롤
    prot = extraction(s1, '단백질') # 단백질

    print("열량 :",energy,"kcal")
    print("나트륨 :",na,"mg")
    print("탄수화물 :",cbh,"g")
    print("   당류 :",sugar,"g")
    print("지방 :",fat,"g")
    print("   트랜스지방 :",transfat,"g")
    print("   포화지방 :",saturatedfat,"g")
    print("콜레스테롤 :",kol,"mg")
    print("단백질 :",prot,"g")

    return energy, na, cbh, sugar, fat, transfat, saturatedfat, kol, prot, str(cautions)
