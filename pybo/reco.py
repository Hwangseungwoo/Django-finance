import pandas as pd

def general_reco(gender, age):
    age = int(age)
    gender = int(gender)
    lst = []
    general_reco = pd.read_csv('./pybo/base/general_reco.csv', encoding='utf-8')
    general_reco = general_reco.drop_duplicates()
    if gender==1:
        sex = "M"
    else:
        sex = "F"
    persona = str(sex)+'_'+str(age)+'_avg'
    temp = pd.DataFrame()
    temp = general_reco[['Jonglyu','GeumYungHoesa','cardNo',persona,'limit']]
    temp = temp.query("limit==0")
    get = pd.DataFrame()
    temp.sort_values(by = persona, ascending=False, inplace=True)
    get = temp.head(3)
    b = get.to_dict('records')
    lst = []
    lst.append(b)
    return lst
    

def personal_reco():
    card = pd.read_csv('./8대영역할당.csv', encoding='utf-8')
    card = card.drop_duplicates()
    personal_info = pd.read_excel('./personal_info_temp.xlsx')
    persona = input("[p1, p2, p3, p4, p5, p6, p7, p8, p9] 중 하나 입력")
    temp = personal_info.copy()
    temp = temp[temp['p']==persona]
    temp.reset_index(inplace=True, drop=True)
    cate = ['직업','학습','건강','관계','주거','사회참여','여가','재무']
    for i in cate:
        card[i] = card[i]*temp[i][0]
    card['score'] =  card['직업']+card['학습']+card['건강']+card['관계']+card['주거']+card['사회참여']+card['여가']+card['재무']
    card = card.query("limit==0")
    card = card[['Jonglyu','GeumYungHoesa','cardNo','score','limit']]
    card.sort_values(by = 'score', ascending=False, inplace=True)
    print(card.head())
    

