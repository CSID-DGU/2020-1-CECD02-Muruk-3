# -*- coding: utf-8 -*-

# main for DTM
#import pandas as pd
#from konlpy.tag import Okt, Kkma
#from sklearn.feature_extraction.text import CountVectorizer
#import numpy as np

#201412
import find_csv as fc
import create_DTM as cDTM
import create_TFIDF as cTF
import create_Apriori as cAP
import visualization as visual

# GUI
print("안녕하세요, 무럭팀 뉴스 키워드 시각화 프로그램입니다.\n")
#print("검색 기간은 2009년 7월부터 2019년 4월 이내로 제공합니다.\n")
period = input("검색하고자 하는 달을 입력하세요(ex. 202010) >> ")

gisa_keyword_df1, gisa_keyword_df2, gisa_keyword_df3, gisa_keyword_df4, gisa_keyword_df5, yyyy, mm = fc.find_csv_sepearte_week(period)

gisa_content_week1 = []
gisa_content_week2 = []
gisa_content_week3 = []
gisa_content_week4 = []

if not gisa_keyword_df5.empty: #값이 있으면 실행, 값이 없으면 실행하지 않음
  gisa_content_week5 = []
  for line5 in gisa_keyword_df5['기사 내용']:
    gisa_content_week5.append(line5)
  cDTM.make_DTM_file(gisa_content_week5, yyyy, mm, 5)

for line1 in gisa_keyword_df1['기사 내용']:
  gisa_content_week1.append(line1)
for line2 in gisa_keyword_df2['기사 내용']:
  gisa_content_week2.append(line2)
for line3 in gisa_keyword_df3['기사 내용']:
  gisa_content_week3.append(line3)
for line4 in gisa_keyword_df4['기사 내용']:
  gisa_content_week4.append(line4)

cDTM.make_DTM_file(gisa_content_week1, yyyy, mm, 1)
cDTM.make_DTM_file(gisa_content_week2, yyyy, mm, 2)
cDTM.make_DTM_file(gisa_content_week3, yyyy, mm, 3)
cDTM.make_DTM_file(gisa_content_week4, yyyy, mm, 4) # 12/28 None

cTF.create_TFIDF(period)
cAP.create_Apriori(period)
visual.draw_graph(period)
