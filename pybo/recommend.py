import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# read -> finan_data & insur_data(return = list) 
# -> obj_insur(성별,나이, insur_data로 리턴받은 list) 하면 이제 return값 = 나이, 성별에 맞는 보험 리스트
# 이 단계 이후 return list = 최초 추천 상품 list 도출

# reading csvs
def read():
    # insurance
    a = pd.read_csv('./pybo/base/cat_df.csv') # cat_df, 성별 나이별 각 보험 보유 비율
    b = pd.read_csv('./pybo/base/bj_df.csv') # bj_df, 보장내용, 보장금액, 영역
    c = pd.read_csv('./pybo/base/ts_df.csv') # ts_df, 분류,설명,제목(라벨링)
    d = pd.read_csv('./pybo/base/total_df.csv', encoding='utf-8') # total_df. 전체데이터, 가입기준
    p = pd.read_csv('./pybo/base/yj_df.csv')
    d['보험료'] = d['보험료'].str.replace(pat=r',', repl= r'', regex=True)  # replace all special symbols to space
    d['보험료']=pd.to_numeric(d['보험료'])
    d['최소연령']=0
    d['최대연령']=100
    for i in range(len(d)):
      w = []
      if type(d.iloc[i].가입연령) == float:
          continue
      w = d.iloc[i].가입연령.split('~')
      d.loc[i, '최소연령'] = w[0]
      d.loc[i, '최대연령'] = w[1]
    o = pd.read_csv('./pybo/base/cat_df_ - cat_df_.csv')
    d = pd.merge(d,o,how='inner', on=['상품명','회사명','분류','분류코드'])

    # finan
    e = pd.read_csv('./pybo/base/채권.csv') # 채권 가중치 재무100 15241, 재무70주거30 68
    f = pd.read_csv('./pybo/base/펀드.csv') # 펀드 가중치 재무100 724. 재무50주거50 116
    g = pd.read_csv('./pybo/base/연금저축.csv') # 연금 가중치 주거100 2043
    h = pd.read_csv('./pybo/base/원리금보장 연금저축보험.csv') # 원리금보장 연금저축보험 주거100 51
    u = pd.read_csv('./pybo/base/원리금보장 퇴직연금.csv') # 원리금보장 퇴직연금 주거100 1121
    return a,b,c,d,o,p,e,f,g,h,u

# get recommend item of finance data, type list의 list
def obj_finan(e,f,g,h,u):
    finan_list = []
    #채권, CoupnRt 기준 3개 추출
    share_1 = pd.DataFrame()
    share_2 = pd.DataFrame()
    #재무100 중에서
    #종가수익률 기준으로 정렬
    e1 = e[e.재무==100].sort_values(by='종가_수익률',ascending=False)
    share_1 = e1.head(3)
    #재무70,주거30 중에서
    #종가수익률 기준으로 정렬
    e2 = e[e.재무!=100].sort_values(by='종가_수익률',ascending=False)
    share_2 = e2.head(3)
    finan_list.append(share_1.to_dict('records'))
    finan_list.append(share_2.to_dict('records'))

    #펀드, VAssetsCmpsEtcRt 기준 3개 추출
    fund_1 = pd.DataFrame()
    fund_2 = pd.DataFrame()
    #재무100중에서
    #3년수익률, 1년수익률, 6개월수익률 기준으로 정렬
    f1 = f[f.재무==100].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
    fund_1 = f1.head(3)
    #재무50,주거50중에서
    #3년수익률, 1년수익률, 6개월수익률 기준으로 정렬
    f2 = f[f.재무!=100].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
    fund_2 = f2.head(3)
    finan_list.append(fund_1.to_dict('records'))
    finan_list.append(fund_2.to_dict('records'))
    
    #연금, Reserves 기준 3개 추출
    #전년도수익률,장기수익률 기준으로 정렬
    pension = pd.DataFrame()
    g1 = g.sort_values(by=['전년도_수익률','장기수익률(연평균)_3년'],ascending=False)
    pension = g1.head(3)
    finan_list.append(pension.to_dict('records'))
    
    #원리금보장 연금저축보험, CoupnRt 기준 3개 추출
    #공시이율 기준으로 정렬
    save = pd.DataFrame()
    h1 = h.sort_values(by='공시이율',ascending=False)
    save = h1.head(3)
    finan_list.append(save.to_dict('records'))
    
    # 원리금보장 퇴직연금, 약정금리 기준 3개 추출
    #약정금리 기준으로 정렬
    retired = pd.DataFrame()
    i1 = u.sort_values(by='약정금리',ascending=False)
    retired = i1.head(3)
    finan_list.append(retired.to_dict('records'))
    return finan_list

# 유저의 투자성향 = x
# 적극투자=0, 균형투자=1, 안전투자=2, 보수투자=3
# 적극투자=매우높은위험,높은위험, 균형투자=다소높은위험, 안전투자=보통위험, 보수투자=낮은위험,매우낮은위험
# 만약 투자성향 input이 있을경우
def finan_data_input(x,e,f,g,h,u):
    finan_list = []
    #재무100 중에서
    #종가수익률 기준으로 정렬
    e1 = e[e.재무==100].sort_values(by='종가_수익률',ascending=False)
    share_1 = e1.head(3)
    #재무70,주거30 중에서
    #종가수익률 기준으로 정렬
    e2 = e[e.재무!=100].sort_values(by='종가_수익률',ascending=False)
    share_2 = e2.head(3)
    finan_list.append(share_1.to_dict('records'))
    finan_list.append(share_2.to_dict('records'))

    #펀드, VAssetsCmpsEtcRt 기준 3개 추출
    fund_1 = pd.DataFrame()
    fund_2 = pd.DataFrame()
    #재무100중에서
    #3년수익률, 1년수익률, 6개월수익률 기준으로 정렬
    #재무50,주거50중에서
    #3년수익률, 1년수익률, 6개월수익률 기준으로 정렬
    if x==0:
      f1 = f[(f.재무==100) & ((f.위험=='매우높은위험') | (f.위험 == '높은위험'))].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
      f2 = f[(f.재무!=100) & ((f.위험=='매우높은위험') | (f.위험 == '높은위험'))].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
    elif x==1:
      f1 = f[(f.재무==100) & (f.위험=='다소높은위험')].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
      f2 = f[(f.재무!=100) & (f.위험=='다소높은위험')].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
    elif x==2:
      f1 = f[(f.재무==100) & (f.위험=='보통위험')].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
      f2 = f[(f.재무!=100) & (f.위험=='보통위험')].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
    elif x==3:
      f1 = f[(f.재무==100) & ((f.위험=='매우낮은위험') | (f.위험 == '낮은위험'))].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
      f2 = f[(f.재무!=100) & ((f.위험=='매우낮은위험') | (f.위험 == '낮은위험'))].sort_values(by=['3년 수익률','1년 수익률','6개월 수익률'],ascending=False)
    fund_1 = f1.head(3)
    fund_2 = f2.head(3)
    finan_list.append(fund_1.to_dict('records'))
    finan_list.append(fund_2.to_dict('records'))
    
    #연금, Reserves 기준 3개 추출
    #전년도수익률,장기수익률 기준으로 정렬
    
    pension = pd.DataFrame()
    if x == 0:
      g1 = g[(g.위험=='매우높은위험') | (g.위험=='높은위험')].sort_values(by=['전년도_수익률','장기수익률(연평균)_3년'],ascending=False)
    elif x == 1:
      g1 = g[g.위험==('다소높은위험')].sort_values(by=['전년도_수익률','장기수익률(연평균)_3년'],ascending=False)
    elif x == 2:
      g1 = g[g.위험==('보통위험')].sort_values(by=['전년도_수익률','장기수익률(연평균)_3년'],ascending=False)
    elif x == 3:
      g1 = g[(g.위험=='매우낮은위험' ) | (g.위험== '낮은위험')].sort_values(by=['전년도_수익률','장기수익률(연평균)_3년'],ascending=False)
    pension = g1.head(3)
    finan_list.append(pension.to_dict('records'))
    
    #원리금보장 연금저축보험, CoupnRt 기준 3개 추출
    #공시이율 기준으로 정렬
    save = pd.DataFrame()
    h1 = h.sort_values(by='공시이율',ascending=False)
    save = h1.head(3)
    finan_list.append(save.to_dict('records'))
    
    #원리금보장 퇴직연금, 약정금리 기준 3개 추출
    #약정금리 기준으로 정렬
    retired = pd.DataFrame()
    i1 = u.sort_values(by='약정금리',ascending=False)
    retired = i1.head(3)
    finan_list.append(retired.to_dict('records'))
    return finan_list
  
#보험료 기준으로 정렬
# get recommend item of insurance data, type list의 list
def insur_data(d):
    insur_list = []
    q1 = d[d.분류코드==1].sort_values(by='보험료')
    d_1 = q1.head(3)
    a = d_1.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q2 = d[d.분류코드==2].sort_values(by='보험료')
    d_2 = q2.head(3)
    a = d_2.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q3 = d[d.분류코드==3].sort_values(by='보험료')
    d_3 = q3.head(3)
    a = d_3.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q4 = d[d.분류코드==4].sort_values(by='보험료')
    d_4 = q4.head(3)
    a = d_4.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q5 = d[d.분류코드==5].sort_values(by='보험료')
    d_5 = q5.head(3)
    a = d_5.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q6 = d[d.분류코드==6].sort_values(by='보험료')
    d_6 = q6.head(3)
    a = d_6.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q7 = d[d.분류코드==7].sort_values(by='보험료')
    d_7 = q7.head(3)
    a = d_7.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q8 = d[d.분류코드==8].sort_values(by='보험료')
    d_8 = q8.head(3)
    a = d_8.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q9 = d[d.분류코드==9].sort_values(by='보험료')
    d_9 = q9.head(3)
    a = d_9.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q10 = d[d.분류코드==10].sort_values(by='보험료')
    d_10 = q10.head(3)
    a = d_10.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q11 = d[d.분류코드==11].sort_values(by='보험료')
    d_11 = q11.head(3)
    a = d_11.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q12 = d[d.분류코드==12].sort_values(by='보험료')
    d_12 = q12.head(3)
    a = d_12.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q13 = d[d.분류코드==13].sort_values(by='보험료')
    d_13 = q13.head(3)
    a = d_13.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q14 = d[d.분류코드==14].sort_values(by='보험료')
    d_14 = q14.head(3)
    a = d_14.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q15 = d[d.분류코드==15].sort_values(by='보험료')
    d_15 = q15.head(3)
    a = d_15.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q16 = d[d.분류코드==16].sort_values(by='보험료')
    d_16 = q16.head(3)
    a = d_16.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q17 = d[d.분류코드==17].sort_values(by='보험료')
    d_17 = q17.head(3)
    a = d_17.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q18 = d[d.분류코드==18].sort_values(by='보험료')
    d_18 = q18.head(3)
    a = d_18.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q19 = d[d.분류코드==19].sort_values(by='보험료')
    d_19 = q19.head(3)
    a = d_19.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    q99 = d[d.분류코드==99].sort_values(by='보험료')
    d_99 = q99.head(3)
    a = d_99.to_dict('records')
    if a == '':
      a == 'NULL'
    insur_list.append(a)
    return insur_list

# insurance
# x for gender, y for age
# assume x = 1 -> man, x=2 -> woman
# age는 출생년도가 아닌 나이로 들어온다고 가정
# return 값 = 각 나이대별 대표 보험 리스트
def obj_insur(x,y, list):
    if x==1:
        gender = 'm_'
    else:
        gender = 'f_'

    if y<20:
        age = '10'
    elif y>=70:
        age = '70'
    else:
        if y%10<5:
            age = str((y//10)*10)+'_1'
        else:
            age = str((y//10)*10)+'_2'

    cla = gender+age

    return classify(cla, list)
  
  
def classify(a, list):
    list1 = ['m_10','m_20_1','w_10','w_20_1']
    list2 = ['w_20_2']
    list3 = ['m_20_2']
    list4 = ['m_30_1','m_30_2','m_40_1','m_40_2','w_30_1']
    insur_lis = []
    if a in list1:
        insur_lis.append(list[2])
        insur_lis.append(list[3])
        insur_lis.append(list[6])
        return (insur_lis)
    elif a in list2:
        insur_lis.append(list[0])
        insur_lis.append(list[2])
        insur_lis.append(list[3])
        insur_lis.append(list[6])
        return (insur_lis)
    elif a in list3:
        insur_lis.append(list[0])
        insur_lis.append(list[2])
        insur_lis.append(list[3])
        insur_lis.append(list[6])
        insur_lis.append(list[12])
        return (insur_lis)
    elif a in list4:
        insur_lis.append(list[0])
        insur_lis.append(list[2])
        insur_lis.append(list[3])
        insur_lis.append(list[12])
        return (insur_lis)
    else:
        insur_lis.append(list[2])
        insur_lis.append(list[3])
        insur_lis.append(list[12])
        return (insur_lis)
    
# 문장유사도 검사
def similar_cosine(a,b):
    sent= (a,b)     
    # 객체 생성
    tfidf_vectorizer = TfidfVectorizer()

    # 문장 벡터화 진행
    tfidf_matrix = tfidf_vectorizer.fit_transform(sent)

    # 각 단어
    text = tfidf_vectorizer.get_feature_names()

    # 각 단어의 벡터 값
    idf = tfidf_vectorizer.idf_

    # 코사인 유사도
    df = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return df[0][0]

# a for 목표
# 목표와 상품명 간 유사도 검사
def goal_insu(a,d):
    lost = []
    sim = []
    new = d
    new['유사도']=0
    for i in range(len(new)):
      lost.append(str(new.iloc[i].상품명))
    lost = [str(item) for item in lost]
    for i in range(len(new)):
      cos_sim = similar_cosine(a,lost[i])
      new.loc[i, '유사도']=cos_sim
      new = new.sort_values(by=['유사도','보험료'],ascending = [False,True])
    if new.iloc[0].유사도==0:
      new['유사도']=0
      d = new

# a=성별 / b=나이 / c=목표 / d = 영역
def cal_insur(sex, age, goal, category,d):
  # 가입연령 맞는 나이 보험 추출
  d = d[(d.최소연령.astype(int)<=int(age)) & (d.최대연령.astype(int)>=int(age))]

  # 대표 카테고리가 포함되는지 확인
  if '종신' in goal:
    recom = d[(d.분류코드==1)].sort_values(by='보험료').head(3)
  elif '정기' in goal:
    recom = d[(d.분류코드==2)].sort_values(by='보험료').head(3)
  elif (('질병' in goal) or ('건강' in goal)):
    recom = d[(d.분류코드==3)].sort_values(by='보험료').head(3)
  elif '상해' in goal:
    recom = d[(d.분류코드==4)].sort_values(by='보험료').head(3)
  elif '암' in goal:
    recom = d[(d.분류코드==5)].sort_values(by='보험료').head(3)
  elif (('간병' in goal) or ('요양' in goal)):
    recom = d[(d.분류코드==6)].sort_values(by='보험료').head(3)
  elif '어린이' in goal:
    recom = d[(d.분류코드==7)].sort_values(by='보험료').head(3)
  elif '치아' in goal:
    recom = d[(d.분류코드==8)].sort_values(by='보험료').head(3)
  elif (('저축' in goal) or ('양로' in goal)):
    recom = d[(d.분류코드==11)].sort_values(by='보험료').head(3)
  elif '운전' in goal:
    recom = d[(d.분류코드==13)].sort_values(by='보험료').head(3)
  elif '여행' in goal:
    recom = d[(d.분류코드==14)].sort_values(by='보험료').head(3)
  elif '골프' in goal:
    recom = d[(d.분류코드==15)].sort_values(by='보험료').head(3)
  elif (('화재' in goal) or ('재물' in goal)):
    recom = d[(d.분류코드==18)].sort_values(by='보험료').head(3)

  # 대표키워드 포함 안될시
  else:
    # 문장 유사도 검색
    goal_insu(goal,d)

    # 유사도 결과가 전부 0이 아니면
    if d.iloc[0].유사도!=0:
      recom = d.head(3)
    
    # 유사도가 전부 0이면 영역별 비율로 추출
    else:
      d = d.sort_values(by=[category,'보험료'],ascending=[False,True])
      recom = d.head(3)

  goal_insur_list = []
  a = recom.to_dict('records')
  if a == '':
    a == 'NULL'
  goal_insur_list.append(a)
  return goal_insur_list

# input 나이, 성별, 설정목표, 목표설정카테고리, 투자성향
# gender는 남자는 1, 여자는 2
def final_get(age,gender,goal,category,trait):
  a,b,c,d,o,p,e,f,g,h,u = read()
  age = int(age)
  gender = int(gender)
  trait = int(trait)
  
  no_trait_finan_list = []
  no_trait_finan_list = obj_finan(e,f,g,h,u)
  trait_finan_list = []
  if trait is not None:
    trait_finan_list = finan_data_input(trait,e,f,g,h,u)
  
  insur_list = []
  insur_list = insur_data(d)
  no_input_insur_list = []
  no_input_insur_list = obj_insur(gender,age,insur_list)
  input_inusr_list = []
  input_inusr_list = cal_insur(gender,age,goal,category,d)
  return no_trait_finan_list,trait_finan_list,no_input_insur_list,input_inusr_list
  
  
      
      
