# -*- coding: utf-8 -*-

# DTM을 csv 파일로 저장하는 함수
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
import os
import pandas as pd


def make_DTM_file(gisa_content, yyyy, mm, week):
    # 우선 만들어진 파일이 있는지 확인하는 코드
    #dir = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/김민선/DTM/' + str(yyyy) + '_' + str(mm)
    dir = './data_storage/DTM/' + str(yyyy) + '_' + str(mm)

    if os.path.exists(dir):  # 해당 폴더가 존재하면
        csv_list = os.listdir(dir)
        if len(csv_list) >= 4:  # 안의 파일의 크기가 4개보다 더 크면
            if week == 1:
                print("... ### DTM 파일 읽어오는 중 ### ...")
            # tmp_pd = pd.DataFrame()
            # tmp_pd = pd.read_csv(dir + '/' + csv_list[week-1], index_col = 0)
            # print(tmp_pd)
            return None
        else:
            if week == 1:
                print("... ### DTM 파일 생성 중 ... ###")
    okt = Okt()
    cv = CountVectorizer()

    # print(gisa_content)

    nouns = []
    nouns_list = []

    # 불용어 txt 불러오기
    #file = open('/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/유주은/StopWords.txt', 'r')
    file = open('./data_storage/StopWords.txt', 'r', encoding='utf-8')
    stop_file = file.read()
    file.close()

    # 명사 추출 + 불용어 제거
    for doc in gisa_content:
        nouns = okt.nouns(doc)
        nouns = [word for word in nouns if not word in stop_file]
        nouns_list.append(' '.join(nouns))

    DTM_Array = cv.fit_transform(nouns_list).toarray()
    feature_names = cv.get_feature_names()
    DTM_DataFrame = pd.DataFrame(DTM_Array, columns=feature_names)

    #directory = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/김민선/DTM/' + str(yyyy) + '_' + str(mm)
    directory = './data_storage/DTM/' + str(yyyy) + '_' + str(mm)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

    DTM_DataFrame.to_csv(directory + '/' + str(yyyy) + '_' + str(mm) + '_week' + str(week) + '_DTM.csv',
                         encoding='utf-8')  # ''에 csv 생성할 파일 이름 입력