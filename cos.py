from konlpy.tag import Okt
import numpy as np
from numpy import dot
from numpy.linalg import norm
import database.mariaDB as mariaDB
from database.mariaDB import conn

# 코사인 유사도를 구하는 함수
def cos_sim(A, B):
    norm_A = norm(A)
    norm_B = norm(B)

    if norm_A == 0 or norm_B == 0:
        return 0.0

    return dot(A, B)/(norm(A)*norm(B))


# 기준이 되는 키워드와 벡터 키워드 리스트를 받아서 키워드별 빈도를 구하는 함수
def make_matrix(feats, list_data):
    freq_list = []
    for feat in feats:
        freq = 0
        for word in list_data:
            if feat == word:
                freq += 1
        freq_list.append(freq)
    return freq_list

def check_preference(result, food_ingredients, food_name):

    food_ingredients_data = []

    for i in range(0, len(food_ingredients)):
        food_ingredients_data.append(food_ingredients[i])
        food_ingredients_data[i] = ''.join(map(str, food_ingredients_data[i]))

    preference_food = ''.join(map(str, result))

    okt = Okt()

    preference_food = okt.nouns(preference_food)

    for i in range(0, len(food_ingredients_data)):
        food_ingredients_data[i] = okt.nouns(food_ingredients_data[i])

    v4 = []
    v4 += preference_food

    for i in range(0, len(food_ingredients_data)):
        v4 += food_ingredients_data[i]

    feats = set(v4)

    preference_food_arr = np.array(make_matrix(feats, preference_food))
    test_arr = []
    cs_arr = []

    for i in range(0, len(food_ingredients_data)):
        test_arr.append(np.array(make_matrix(feats, food_ingredients_data[i])))
        cs_arr.append(cos_sim(preference_food_arr, test_arr[i]))

    sorted_pairs = sorted([(cs_arr[i], food_name[i]) for i in range(len(cs_arr)) if cs_arr[i] != 0], reverse=True)
    sorted_food_name = [pair[1] for pair in sorted_pairs]

    return sorted_food_name[:min(6, len(sorted_food_name))]
    