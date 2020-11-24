# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfTransformer
import os
import pandas as pd
import numpy as np

def create_TFIDF(yyyymm):
    yyyy = str(yyyymm)[:4]
    mm = str(yyyymm)[4:]
    if mm[0] == '0':
        mm = mm[1]

        # 우선 만들어진 파일이 있는지 확인하는 코드
    #dir = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/유주은/수정중_표준편차/' + str(yyyy) + '_' + str(mm)  # + '_'
    dir = './data_storage/TFIDF_SD/' + str(yyyy) + '_' + str(mm)  # + '_'

    if os.path.exists(dir):  # 해당 폴더가 존재하면
        csv_list = os.listdir(dir)
        if len(csv_list) >= 4:  # 안의 파일의 크기가 4개보다 더 크면
            print("... ### TF-IDF 파일 읽어오는 중 ... ###")
            tmp_pd = pd.DataFrame()
            # for i in csv_list :
            # tmp_pd = pd.read_csv(dir + '/' + i, index_col = 0)
            # print(tmp_pd)
            return None
        else:
            None

            #dir = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/김민선/DTM/'
    dir = './data_storage/DTM/'

    # yyyy = str(yyyymm)[:4]
    # mm = str(yyyymm)[4:]
    # if mm[0] == '0':
    #  mm = mm[1]
    csv_dir = dir + yyyy + '_' + mm
    csv_list = os.listdir(csv_dir)
    csv_list.sort()
    week_num = 1
    for i in csv_list:
        tmp_pd = pd.read_csv(csv_dir + '/' + i, index_col=0, encoding='utf-8')  # 한 주의 DTM 파일을 읽어옴
        tmp_pd.pop(tmp_pd.columns[0])

        # 사이킷런을 이용하여 TFIDF 생성 https://wikidocs.net/31698
        tfidf = TfidfTransformer().fit_transform(tmp_pd)
        tfidf_array = tfidf.toarray()
        tfidf_data_frame = pd.DataFrame(tfidf_array, columns=tmp_pd.columns)
        '''
        #directory = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/유주은/수정중_RANK/' + str(yyyy) + '_' + str(mm)  # + '_'
        directory = './data_storage/TFIDF_RANK/' + str(yyyy) + '_' + str(mm)
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory. ' + directory)
        '''
        # 1. TF-IDF RANK 구하기  - 각각 모든 문서에 대해서임 1080개 있으면 1080개 다
        rank_df = pd.DataFrame()

        for index in range(len(tfidf_data_frame)):
            df1 = tfidf_data_frame[index:index + 1].T
            df1_sort = df1.sort_values(by=index, ascending=False)  # tf-idf값 높은 순서대로 정렬
            df1_high = df1_sort.head(30)  # 상위 30위
            # print(df1_high)
            df_rank = df1_high.rank(method='first', ascending=False)  # 순위 매김
            df2 = df_rank.T
            rank_df = rank_df.append(df2)

        rank_df = rank_df.fillna(0)  # NaN값 처리

        # 2. TF-IDF 표준편차 구하기
        sample_df = pd.DataFrame()

        # 2) 키워드의 표준편차 구하기
        rank_var = np.var(rank_df)
        rank_22 = rank_var.sort_values(ascending=False)  # 높은 순서대로 표준편차
        rank_true = (rank_22 >= 1)  # 표준편차 1 이상인 키워드 = True

        stop_keyword = []

        # 표준편차 1 넘지 못하는 단어들 --> 불용어 수준의 단어들 = stop_keyword
        print("불용어 수준의 단어들 : ")
        for i in range(len(rank_true)):
            if (rank_true[i] == False):  # 표준편차 1 이하인 단어들 = False
                rank_true.index[i]
                # print(rank_true.index[i])
                stop_keyword.append(rank_true.index[i])  # stop_keyword들임

        sample_df = rank_df

        # 불용어 수준의 단어들 제거 - stop_keyword
        for j in range(len(rank_df.columns)):
            for stop_key in stop_keyword:
                if (rank_df.columns[j] == stop_key):
                    # print(rank_df.columns[j])
                    # print("--", j)
                    # print("--",stop_key)
                    #print(stop_key)
                    # print(rank_df[rank_df.columns[j]])
                    sample_df = sample_df.drop([rank_df.columns[j], ], axis=1)
                    # print(sample_df)
        print(sample_df)

        #directory2 = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/유주은/수정중_표준편차/' + str(yyyy) + '_' + str(mm)  # + '_'
        directory2 = './data_storage/TFIDF_SD/' + str(yyyy) + '_' + str(mm)
        try:
            if not os.path.exists(directory2):
                os.makedirs(directory2)
        except OSError:
            print('Error: Creating directory. ' + directory2)
        sample_df.to_csv(directory2 + '/' + yyyy + '_' + mm + '_' + 'week' + str(week_num) + '_TF-IDF.csv', encoding='utf-8')  # 중간에 '_'
        week_num = week_num + 1