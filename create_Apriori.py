# -*- coding: utf-8 -*-

import os
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


def create_Apriori(yyyymm):
    yyyy = str(yyyymm)[:4]
    mm = str(yyyymm)[4:]
    if mm[0] == '0':
        mm = mm[1]

        # 우선 만들어진 파일이 있는지 확인하는 코드
    #dir = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/김민선/Apriori/' + str(yyyy) + '_' + str(mm)  # + '_'
    dir = './data_storage/Apriori/' + str(yyyy) + '_' + str(mm)

    if os.path.exists(dir):
        csv_list = os.listdir(dir)
        print("... ### Apriori 파일 읽어오는 중 ### ...")
        tmp_pd = pd.read_csv(dir + '/' + csv_list[0], index_col=0)
        #print(tmp_pd)201
        return None

    print("... ### Apriori 파일 생성 중 ... ###")

    #dir = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/유주은/수정중_표준편차/'
    dir = './data_storage/TFIDF_SD/'

    gisa_df = pd.DataFrame()
    # yyyy = str(yyyymm)[:4]
    # mm = str(yyyymm)[4:]
    # if mm[0] == '0':
    #  mm = mm[1]
    csv_dir = dir + yyyy + '_' + mm
    csv_list = os.listdir(csv_dir)
    csv_list.sort()

    for i in csv_list:
        tmp_pd = pd.read_csv(csv_dir + '/' + i, index_col=0, encoding='utf-8')  # 한 주의 DTM 파일을 읽어옴
        gisa_df = gisa_df.append(tmp_pd)

    gisa_df = gisa_df.fillna(0)  # 4~5주치의 DFIDF 결과를 합쳤을 때, NaN값 처리

    gisa_df[gisa_df < 0] = False
    gisa_df[gisa_df >= 1] = True

    frequent = apriori(gisa_df, min_support=0.01, use_colnames=True)
    final_frequent_2 = pd.DataFrame()

    # 단어가 두개인것만 추출한다
    for x, y, z in zip(range(len(frequent)), list(frequent['itemsets']), frequent['support']):
        if (len(y) == 2):
            #print(type(frequent))
            line = {'support': z, 'itemsets': y}
            final_frequent_2 = final_frequent_2.append(line, ignore_index=True)

    #print(final_frequent_2)

    directory = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/김민선/Apriori/' + str(yyyy) + '_' + str(mm)  # + '_'
    directory = './data_storage/Apriori/' + str(yyyy) + '_' + str(mm)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

    final_frequent_2.to_csv(directory + '/' + yyyy + '_' + mm + '_final2.csv', encoding='utf-8')