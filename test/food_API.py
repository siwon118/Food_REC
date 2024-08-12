import requests
import xmltodict
import json

# 음식코드, 대분류, 중분류, 음식명
url = 'http://apis.data.go.kr/1390802/AgriFood/MzenFoodCode/getKoreanFoodList'
params ={'serviceKey' : 'm3kguEAbr0noWcr%2FRxbglv96p1HJl3zLDcwQkVr2m7Wzx4SNORuK5nWYOaVJMcbrYZ6EwOt1dCb4gtu3dw%2FZug%3D%3D',
         'Page_No' : '1',
         'Page_Size' : '30',
         #'food_Group_Code' : '06',             #음식 분류 코드 (ex. 찌개류, 밥류)
         'food_Name' : '비빔밥' }

response = requests.get(url, params=params)

hotspots_data = response.content
data_dict = xmltodict.parse(hotspots_data)      # convert xml to dict
json_data = json.loads(json.dumps(data_dict))   # convert to json

data_list_1 = None
# data_list_1_food_Code = None
# data_list_1_large_Name = None
# data_list_1_middle_Name = None
# data_list_1_food_Name = None


for key, value in json_data.items():
    data_list_1 = value.get('body').get('items').get('item')
data_list_1_food_Code = [item['food_Code'] for item in data_list_1]                     # 식품 코드
data_list_1_large_Name = [item['large_Name'] for item in data_list_1]                   # 대분류 명
data_list_1_middle_Name = [item['middle_Name'] for item in data_list_1]                 # 중분류 명
data_list_1_food_Name = [item['food_Name'] for item in data_list_1]                     # 음식명

print('DATA1 식품 코드 :', data_list_1_food_Code)
print('DATA1 대분류 명 :', data_list_1_large_Name)
print('DATA1 중분류 명 :', data_list_1_middle_Name)
print('DATA1 음식명 :', data_list_1_food_Name)
print("-----------------------------------------------------------------------")

#------------------------------------------------------------------------------------------

# #식품 코드로 재료와 영양정보 저장
url = 'http://apis.data.go.kr/1390802/AgriFood/MzenFoodNutri/getKoreanFoodIdntList'
params ={'serviceKey' : 'm3kguEAbr0noWcr%2FRxbglv96p1HJl3zLDcwQkVr2m7Wzx4SNORuK5nWYOaVJMcbrYZ6EwOt1dCb4gtu3dw%2FZug%3D%3D',
         'food_Code' : data_list_1_food_Code[4]}

response2 = requests.get(url, params=params)
hotspots_data = response2.content
data_dict = xmltodict.parse(hotspots_data)      # convert xml to dict
json_data = json.loads(json.dumps(data_dict))   #convert to json

data_list_2 = None
data_list_2_main_Food_Name = None
data_list_2_nutritional_contents = None

for key, value in json_data.items():
    data_list_2 = value.get('body').get('items').get('item')
data_list_2_main_Food_Name = data_list_2.get('main_Food_Name')
data_list_2_nutritional_contents = data_list_2.get('idnt_List')

print('메인 음식:', data_list_2_main_Food_Name)

data_list_2_food_Name = [item['food_Name'] for item in data_list_2_nutritional_contents]        # 식품 명
data_list_2_food_Code = [item['food_Code'] for item in data_list_2_nutritional_contents]        # 식품 코드
food_Weight = [item['food_Weight'] for item in data_list_2_nutritional_contents]                # 식품 중량(g)
energy_Qy = [item['energy_Qy'] for item in data_list_2_nutritional_contents]                    # 에너지(Kcal)
water_Qy = [item['water_Qy'] for item in data_list_2_nutritional_contents]                      # 수분(%)
prot_Qy = [item['prot_Qy'] for item in data_list_2_nutritional_contents]                        # 단백질(g)
ntrfs_Qy = [item['ntrfs_Qy'] for item in data_list_2_nutritional_contents]                      # 지질(g)
ashs_Qy = [item['ashs_Qy'] for item in data_list_2_nutritional_contents]                        # 회분(g)
carbohydrate_Qy = [item['carbohydrate_Qy'] for item in data_list_2_nutritional_contents]        # 탄수화물(g)
sugar_Qy = [item['sugar_Qy'] for item in data_list_2_nutritional_contents]                      # 총 당류(g)
fibtg_Qy = [item['fibtg_Qy'] for item in data_list_2_nutritional_contents]                      # 총 식이섬유(g)
aat19_Qy = [item['aat19_Qy'] for item in data_list_2_nutritional_contents]                      # 총 아미노산(mg)
aae10a_Qy = [item['aae10a_Qy'] for item in data_list_2_nutritional_contents]                    # 필수 아미노산(mg)
aane_Qy = [item['aane_Qy'] for item in data_list_2_nutritional_contents]                        # 비필수 아미노산(mg)
fafref_Qy = [item['fafref_Qy'] for item in data_list_2_nutritional_contents]                    # 총 지방산(g)
faessf_Qy = [item['faessf_Qy'] for item in data_list_2_nutritional_contents]                    # 총 필수 지방산(g)
fasatf_Qy = [item['fasatf_Qy'] for item in data_list_2_nutritional_contents]                    # 총 포화 지방산(g)
famsf_Qy = [item['famsf_Qy'] for item in data_list_2_nutritional_contents]                      # 총 단일 불포화 지방산(g)
fapuf_Qy = [item['fapuf_Qy'] for item in data_list_2_nutritional_contents]                      # 총 다중 불포화 지방산(g)
clci_Qy = [item['clci_Qy'] for item in data_list_2_nutritional_contents]                        # 칼슘(mg)
irn_Qy = [item['irn_Qy'] for item in data_list_2_nutritional_contents]                          # 철(mg)
mg_Qy = [item['mg_Qy'] for item in data_list_2_nutritional_contents]                            # 마그네슘(mg)
phph_Qy = [item['phph_Qy'] for item in data_list_2_nutritional_contents]                        # 인(mg)
ptss_Qy = [item['ptss_Qy'] for item in data_list_2_nutritional_contents]                        # 칼륨(mg)
na_Qy = [item['na_Qy'] for item in data_list_2_nutritional_contents]                            # 나트륨(mg)
zn_Qy = [item['zn_Qy'] for item in data_list_2_nutritional_contents]                            # 아연(mg)
cu_Qy = [item['cu_Qy'] for item in data_list_2_nutritional_contents]                            # 구리(mg)
mn_Qy = [item['mn_Qy'] for item in data_list_2_nutritional_contents]                            # 망간(mg)
se_Qy = [item['se_Qy'] for item in data_list_2_nutritional_contents]                            # 셀레늄(μg)
mo_Qy = [item['mo_Qy'] for item in data_list_2_nutritional_contents]                            # 몰리브덴(μg)
id_Qy = [item['id_Qy'] for item in data_list_2_nutritional_contents]                            # 요오드(μg)
rtnl_Qy = [item['rtnl_Qy'] for item in data_list_2_nutritional_contents]                        # 레티놀(μg)
rtnl_Qy = [item['rtnl_Qy'] for item in data_list_2_nutritional_contents]                        # 베타카로틴(μg)
vitd_Qy = [item['vitd_Qy'] for item in data_list_2_nutritional_contents]                        # 비타민D(D2+D3)(μg)
vite_Qy = [item['vite_Qy'] for item in data_list_2_nutritional_contents]                        # 비타민E(μg)
vitk1_Qy = [item['vitk1_Qy'] for item in data_list_2_nutritional_contents]                      # 비타민K1(μg)
vtmn_B1_Qy = [item['vtmn_B1_Qy'] for item in data_list_2_nutritional_contents]                  # 비타민B1(mg)
vtmn_B2_Qy = [item['vtmn_B2_Qy'] for item in data_list_2_nutritional_contents]                  # 비타민B2(mg)
nacn_Qy = [item['nacn_Qy'] for item in data_list_2_nutritional_contents]                        # 니아신(mg)
pantac_Qy = [item['pantac_Qy'] for item in data_list_2_nutritional_contents]                    # 판토텐산(비타민B5)(mg)
pyrxn_Qy = [item['pyrxn_Qy'] for item in data_list_2_nutritional_contents]                      # 비타민B6(mg)
biot_Qy = [item['biot_Qy'] for item in data_list_2_nutritional_contents]                        # 비오틴(mg)
fol_Qy = [item['fol_Qy'] for item in data_list_2_nutritional_contents]                          # 엽산(μg)
vitb12_Qy = [item['vitb12_Qy'] for item in data_list_2_nutritional_contents]                    # 비타민B12(μg)
vtmn_C_Qy = [item['vtmn_C_Qy'] for item in data_list_2_nutritional_contents]                    # 비타민C(mg)
chole_Qy = [item['chole_Qy'] for item in data_list_2_nutritional_contents]                      # 콜레스테롤(mg)
nacl_Qy = [item['nacl_Qy'] for item in data_list_2_nutritional_contents]                        # 식염상당량(g)


total_Food_Weight = sum(map(float,food_Weight))
total_Energy = sum(map(float,energy_Qy))
total_Water = sum(map(float,water_Qy))
total_Protein = sum(map(float,prot_Qy))
total_Nutrients = sum(map(float,ntrfs_Qy))
total_Ash = sum(map(float,ashs_Qy))
total_Carbohydrate = sum(map(float,carbohydrate_Qy))
total_Sugar = sum(map(float,sugar_Qy))
total_Fiber = sum(map(float,fibtg_Qy))
total_Amino_Acid = sum(map(float,aat19_Qy))
total_Essential_Amino_Acid = sum(map(float,aae10a_Qy))
total_Non_essential_Amino_Acid = sum(map(float,aane_Qy))
total_Fatty_Acid = sum(map(float,fafref_Qy))
total_Essential_Saturated_Fatty_Acid = sum(map(float,faessf_Qy))
total_Saturated_Fatty_Acid = sum(map(float,fasatf_Qy))
total_Monounsaturated_Fatty_Acid = sum(map(float,famsf_Qy))
total_Polyunsaturated_Fatty_Acid = sum(map(float,fapuf_Qy))
total_Calcium = sum(map(float,clci_Qy))
total_Iron = sum(map(float,irn_Qy))
total_Magnesium = sum(map(float,mg_Qy))
total_Phosphorus = sum(map(float,phph_Qy))
total_Potassium = sum(map(float,ptss_Qy))
total_Sodium = sum(map(float,na_Qy))
total_Zinc = sum(map(float,zn_Qy ))
total_Copper = sum(map(float,cu_Qy))
total_Manganese = sum(map(float,mn_Qy))
total_Selenium = sum(map(float,se_Qy))
total_Molybdenum = sum(map(float,mo_Qy))
total_Iodine = sum(map(float,id_Qy))
total_Retinol = sum(map(float,rtnl_Qy))
total_Beta_Carotene = sum(map(float,rtnl_Qy))
total_Vitamin_D = sum(map(float,vitd_Qy))
total_Vitamin_E = sum(map(float,vite_Qy))
total_Vitamin_K1 = sum(map(float,vitk1_Qy))
total_Vitamin_B1 = sum(map(float,vtmn_B1_Qy))
total_Vitamin_B2 = sum(map(float,vtmn_B2_Qy))
total_Niacin = sum(map(float,nacn_Qy))
total_Pantothenic_Acid = sum(map(float,pantac_Qy))
total_Vitamin_B6 = sum(map(float,pyrxn_Qy))
total_Biotin = sum(map(float,biot_Qy))
total_Folate = sum(map(float,fol_Qy))
total_Vitamin_B12 = sum(map(float,vitb12_Qy))
total_Vitamin_C = sum(map(float,vtmn_C_Qy))
total_Cholesterol = sum(map(float,chole_Qy))
total_Equivalent_Salt = sum(map(float,nacl_Qy))




print("재료 명:", data_list_2_food_Name)
print("재료 식품 코드:", data_list_2_food_Code)
# print("재료별영양소------------------------------------------------------------------")
# print("식품 중량(g):", food_Weight)
# print("에너지(kcal):", energy_Qy)
# print("수분(%):", water_Qy)
# print("단백질(g):", prot_Qy)
# print("지질(g):", ntrfs_Qy)
# print("회분(g):", ashs_Qy)
# print("탄수화물(g):", carbohydrate_Qy)
# print("총 당류(g):", sugar_Qy)
# print("총 식이섬유(g):", fibtg_Qy)
# print("총 아미노산(mg):", aat19_Qy)
# print("필수 아미노산(mg):", aae10a_Qy)
# print("비필수 아미노산(mg):", aane_Qy)
# print("총 지방산(g):", fafref_Qy)
# print("총 필수 지방산(g):", faessf_Qy)
# print("총 포화 지방산(g):", fasatf_Qy)
# print("총 단일 불포화 지방산(g):", famsf_Qy)
# print("총 다중 불포화 지방산(g):", fapuf_Qy)
# print("칼슘(mg):", clci_Qy)
# print("철(mg):", irn_Qy)
# print("마그네슘(mg):", mg_Qy)
# print("인(mg):", phph_Qy)
# print("칼륨(mg):", ptss_Qy)
# print("나트륨(mg):", na_Qy)
# print("아연(mg):", zn_Qy)
# print("구리(mg):", cu_Qy)
# print("망간(mg):", mn_Qy)
# print("셀레늄(μg):", se_Qy)
# print("몰리브덴(μg):", mo_Qy)
# print("요오드(μg):", id_Qy)
# print("레티놀(μg):", rtnl_Qy)
# print("베타카로틴(μg):", rtnl_Qy)
# print("비타민D(D2+D3)(μg):", vitd_Qy)
# print("비타민E(μg):", vite_Qy)
# print("비타민K1(μg):", vitk1_Qy)
# print("비타민B1(mg):", vtmn_B1_Qy)
# print("비타민B2(mg):", vtmn_B2_Qy)
# print("니아신(mg):", nacn_Qy)
# print("판토텐산(비타민B5)(mg):", pantac_Qy)
# print("비타민B6(mg):", pyrxn_Qy)
# print("비오틴(mg):", biot_Qy)
# print("엽산(μg):", fol_Qy)
# print("비타민B12(μg):", vitb12_Qy)
# print("비타민C(mg):", vtmn_C_Qy)
# print("콜레스테롤(mg)y:", chole_Qy)
# print("식염상당량(g):", nacl_Qy)
print("-----------------------------------------------------------------------")
print("음식총영양소------------------------------------------------------------------")


# DB에 저장할 영양소----------------------------------------------
print("에너지(kcal):", total_Energy)
print("단백질(g):", total_Protein)
print("총 식이섬유(g):", total_Fiber)
print("비타민C(mg):", total_Vitamin_C)
print("비타민E(μg):", total_Vitamin_E)
print("비타민B1(mg):", total_Vitamin_B1)
print("비타민B2(mg):", total_Vitamin_B2)
print("비타민B6(mg):", total_Vitamin_B6)
print("비타민B12(μg):", total_Vitamin_B12)
print("니아신(mg):", total_Niacin)
print("칼슘(mg):", total_Calcium)
print("나트륨(mg):", total_Sodium)
print("아연(mg):", total_Zinc)


# print("식품 중량(g):", total_Food_Weight)
# print("에너지(kcal):", total_Energy)
# print("수분(%):", total_Water)
# print("단백질(g):", total_Protein)
# print("지질(g):", total_Nutrients)
# print("회분(g):", total_Ash)
# print("탄수화물(g):", total_Carbohydrate)
# print("총 당류(g):", total_Sugar)
# print("총 식이섬유(g):", total_Fiber)
# print("총 아미노산(mg):", total_Amino_Acid)
# print("필수 아미노산(mg):", total_Essential_Amino_Acid)
# print("비필수 아미노산(mg):", total_Non_essential_Amino_Acid)
# print("총 지방산(g):", total_Fatty_Acid)
# print("총 필수 지방산(g):", total_Essential_Saturated_Fatty_Acid)
# print("총 포화 지방산(g):", total_Saturated_Fatty_Acid)
# print("총 단일 불포화 지방산(g):", total_Monounsaturated_Fatty_Acid)
# print("총 다중 불포화 지방산(g):", total_Polyunsaturated_Fatty_Acid)
# print("칼슘(mg):", total_Calcium)
# print("철분(mg):", total_Iron)
# print("마그네슘(mg):", total_Magnesium)
# print("인(mg):", total_Phosphorus)
# print("칼륨(mg):", total_Potassium)
# print("나트륨(mg):", total_Sodium)
# print("아연(mg):", total_Zinc)
# print("구리(mg):", total_Copper)
# print("망간(mg):", total_Manganese)
# print("셀레늄(μg):", total_Selenium)
# print("몰리브덴(μg):", total_Molybdenum)
# print("요오드(μg):", total_Iodine)
# print("레티놀(μg):", total_Retinol)
# print("베타카로틴(μg):", total_Beta_Carotene)
# print("비타민D(D2+D3)(μg):", total_Vitamin_D)
# print("비타민E(μg):", total_Vitamin_E)
# print("비타민K1(μg):", total_Vitamin_K1)
# print("비타민B1(mg):", total_Vitamin_B1)
# print("비타민B2(mg):", total_Vitamin_B2)
# print("니아신(mg):", total_Niacin)
# print("판토텐산(비타민B5)(mg):", total_Pantothenic_Acid)
# print("비타민B6(mg):", total_Vitamin_B6)
# print("비오틴(mg):", total_Biotin)
# print("엽산(μg):", total_Folate)
# print("비타민B12(μg):", total_Vitamin_B12)
# print("비타민C(mg):", total_Vitamin_C)
# print("콜레스테롤(mg):", total_Cholesterol)
# print("식염상당량(g):", total_Equivalent_Salt)
print("-----------------------------------------------------------------------")
#------------------------------------------------------------------------------------------

# 알러지
url = 'http://apis.data.go.kr/1390802/AgriFood/FdFoodCkryImage/getKoreanFoodFdFoodCkryImageList'
params ={'serviceKey' : 'm3kguEAbr0noWcr%2FRxbglv96p1HJl3zLDcwQkVr2m7Wzx4SNORuK5nWYOaVJMcbrYZ6EwOt1dCb4gtu3dw%2FZug%3D%3D',
         'service_Type' : 'xml',
         'Page_No' : '1',
         'Page_Size' : '20',
         #'food_Name' : '감자찌개(고추장)',
         'food_Name' : data_list_2_main_Food_Name,
         #'ckry_Name' : '조리'
         }

response3 = requests.get(url, params=params)



hotspots_data = response3.content
data_dict = xmltodict.parse(hotspots_data)      # convert xml to dict
json_data = json.loads(json.dumps(data_dict))   # convert to json

data_list_3 = None

for key, value in json_data.items():
    data_list_3 = value.get('body').get('items').get('item')

data_list_3_food_Code = data_list_3.get('fd_Code')              # 음식 코드
data_list_3_food_Name = data_list_3.get('fd_Nm')                # 음식명
ckry_Nm = data_list_3.get('ckry_Nm')                            # 조리법명
ckry_Sumry_Info = data_list_3.get('ckry_Sumry_Info')            # 조리법 요약정보


# 중복값 생길 때 인덱스로 찾기-------------------(ex 가지볶음(양파)이 2가지 일때)
# data_list_3_food_Code = data_list_3[0].get('fd_Code')              # 음식 코드
# data_list_3_food_Name = data_list_3[0].get('fd_Nm')                # 음식명
# ckry_Nm = data_list_3[0].get('ckry_Nm')                            # 조리법명
# ckry_Sumry_Info = data_list_3[0].get('ckry_Sumry_Info')            # 조리법 요약정보
#data_list_3_Info = data_list_3[0].get('food_List').get('food')

print('DATA3 음식코드:', data_list_3_food_Code)
print('DATA3 음식명:', data_list_3_food_Name)
# print('DATA3 조리법명:', ckry_Nm)
# print('DATA3 조리법 요약정보:', ckry_Sumry_Info)

data_list_3_Info = data_list_3.get('food_List').get('food')

allergy_Info = [item['allrgy_Info'] for item in data_list_3_Info]    # 알레르기 정보

print('알레르기 정보:', allergy_Info)

#------------------------------------------------------------------------------------------