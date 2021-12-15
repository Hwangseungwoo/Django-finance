import pandas as pd
import numpy as np
import json
from pandas import json_normalize


# data : 상품 raw data
def savings(age, sex):
  df = pd.read_csv("./pybo/base/[저축]적금 _상품조회.csv")
  df = df.sort_values(by=['AfterTaxInterest'])
  # 발급제한 확인
  isRestriction = df['발급제한'] == 0
  df = df[isRestriction]
  # 추천상품 3개 반환
  recom = df.nlargest(3, 'AfterTaxInterest')
  b = recom.to_dict('records')
  lst = []
  lst.append(b)
  return lst

