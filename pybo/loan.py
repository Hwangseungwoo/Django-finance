import pandas as pd
import numpy as np
import json
from pandas import json_normalize


def main_data(sex, age, grade, goal):
    # 목표설정에 대한 가중치
    weights = [0, 0, 0, 0]  # 전세대출, 주택담보대출, 개인신용대출, 중금리대출 가중치
    if ('전세' in goal) or ('주택청약저축' in goal) or ('월세' in goal):
        weights[0] += 1
    if ('집' in goal) or ('주택' in goal):
        weights[1] += 1
    # return 값은 출력 방식에 맞게 조정
    # 가중치 순서대로 출력
    if weights[0]>weights[1]:
        lst1 = deposit_loan(sex, age)
        lst2 = mortgage_loan(sex, age)
    else:
        lst1 = mortgage_loan(sex, age)
        lst2 = deposit_loan(sex, age)
    
    lst3 = private_loan(sex, age)
    lst4 = midinterest_loan(sex, age, grade)
    return lst1,lst2,lst3,lst4


def income(grade):
    if grade == '1':
        return 0
    elif grade == '2':
        return 2000
    elif grade == '3':
        return 3000
    elif grade == '4':
        return 4000
    elif grade == '5':
        return 5000
    elif grade == '6':
        return 6000
    else:
        return 7000

# data : 상품 raw data
def deposit_loan(age, sex):
    df = pd.read_csv("./pybo/base/[대출상품]전세자금대출_상품조회.csv")
    df['score'] = pd.to_numeric(df['LendRateAvg'].str[:-1])
    df = df.sort_values(by=['score'])
    # 추천상품 3개 반환
    recom = df.nsmallest(3, 'score')
    a = recom.to_dict('records')
    lst = []
    lst.append(a)
    return lst

# data : 상품 raw data
def mortgage_loan(age, sex):
    df = pd.read_csv("./pybo/base/[대출상품]주택담보대출_상품조회.csv")
    df['score'] = pd.to_numeric(df['LendRateMin'].str[:-1])
    df = df.sort_values(by=['score'])
    # 추천상품 3개 반환
    recom = df.nsmallest(3, 'score')
    a = recom.to_dict('records')
    lst = []
    lst.append(a)
    return lst

# data : 상품 raw data
def private_loan(age, sex):
    df = pd.read_csv("./pybo/base/[대출상품]개인신용대출_상품조회.csv")
    df['score'] = pd.to_numeric(df['LendRateAvg'].str[:-1])
    df = df.sort_values(by=['score'])
    # 추천상품 3개 반환
    recom = df.nsmallest(3, 'score')
    a = recom.to_dict('records')
    lst = []
    lst.append(a)
    return lst

# data : 상품 raw data
def midinterest_loan(age, sex, grade):
    df = pd.read_csv("./pybo/base/[대출상품]중금리신용대출_저축은행_상품조회.csv")
    df = df.sort_values(by=['Credit5AveRate'])
    # 발급제한 확인
    isIncome = df['연소득(단위:만)'] < income(grade)
    isRestriction = df['제한(1:제한,0:제한없음)'] == 0
    df = df[isIncome & isRestriction]
    # 추천상품 3개 반환
    recom = df.nsmallest(3, 'Credit5AveRate')
    a = recom.to_dict('records')
    lst = []
    lst.append(a)
    return lst


