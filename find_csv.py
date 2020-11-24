# -*- coding: utf-8 -*-

import pandas as pd
import os

def find_csv_sepearte_week(yyyymm):

    print("\n... ### 뉴스 기사 읽어오는 중 ... ###")
    #dir = '/content/drive/My Drive/뉴스분석_소스코드/01. 크롤링/김민선/Date'
    #dir = './crawling_data'
    dir = './crawling_data'

    gisa_df1 = pd.DataFrame()
    gisa_df2 = pd.DataFrame()
    gisa_df3 = pd.DataFrame()
    gisa_df4 = pd.DataFrame()
    gisa_df5 = pd.DataFrame()

    yyyy = str(yyyymm)[:4]
    mm = str(yyyymm)[4:]
    if mm[0] == '0':
        mm = mm[1]
    csv_dir = dir + '/' + yyyy + '년/' + mm + '월'
    csv_list = os.listdir(csv_dir)

    thirty = ['4', '6', '9', '11']  # 2월은 28일
    thirty_one = ['1', '3', '5', '7', '8', '10', '12']

    day = 0

    if mm == '2':
        day = 28
        #print("28일")
    elif mm in thirty:
        day = 30
        #print("30일")
    elif mm in thirty_one:
        day = 31
        #print("31일")

    for j1 in range(0, 7):  # 1, 2, 3, 4, 5, 6, 7
        tmp_pd1 = pd.read_csv(csv_dir + '/' + csv_list[j1], index_col=0, encoding='utf-8')
        gisa_df1 = gisa_df1.append(tmp_pd1)
        # print(gisa_df1)

    for j2 in range(7, 14):  # 8, 9, 10, 11, 12, 13, 14
        tmp_pd2 = pd.read_csv(csv_dir + '/' + csv_list[j2], index_col=0, encoding='utf-8')
        gisa_df2 = gisa_df2.append(tmp_pd2)
        # print(gisa_df2)

    for j3 in range(14, 21):  # 15, 16, 17, 18, 19, 20, 21
        tmp_pd3 = pd.read_csv(csv_dir + '/' + csv_list[j3], index_col=0, encoding='utf-8')
        gisa_df3 = gisa_df3.append(tmp_pd3)
        # print(gisa_df3)

    for j4 in range(21, 28):  # 22, 23, 24, 25, 26, 27, 28
        tmp_pd4 = pd.read_csv(csv_dir + '/' + csv_list[j4], index_col=0, encoding='utf-8')
        gisa_df4 = gisa_df4.append(tmp_pd4)
        # print(gisa_df4)

    if (day == 30):
        for j5 in range(28, 30):  # 29, 30
            tmp_pd5 = pd.read_csv(csv_dir + '/' + csv_list[j5], index_col=0, encoding='utf-8')
            gisa_df5 = gisa_df5.append(tmp_pd5)
            graph_info_5 = gisa_df5[['기사 제목', '기사 링크', '기사 내용']]

    elif (day == 31):
        for j5 in range(28, 31):  # 29, 30, 31
            tmp_pd5 = pd.read_csv(csv_dir + '/' + csv_list[j5], index_col=0, encoding='utf-8')
            gisa_df5 = gisa_df5.append(tmp_pd5)
            graph_info_5 = gisa_df5[['기사 제목', '기사 링크', '기사 내용']]

    gisa_df1.reset_index(drop=True, inplace=True)
    gisa_df2.reset_index(drop=True, inplace=True)
    gisa_df3.reset_index(drop=True, inplace=True)
    gisa_df4.reset_index(drop=True, inplace=True)

    if not gisa_df5.empty:  # 5주차가 비어있지 않으면
        gisa_df5.reset_index(drop=True, inplace=True)

    else:
        gisa_df5 = pd.DataFrame()

    # 민선 추가
    graph_info_1 = gisa_df1[['기사 제목', '기사 링크', '기사 내용']]
    graph_info_2 = gisa_df2[['기사 제목', '기사 링크', '기사 내용']]
    graph_info_3 = gisa_df3[['기사 제목', '기사 링크', '기사 내용']]
    graph_info_4 = gisa_df4[['기사 제목', '기사 링크', '기사 내용']]
    # graph_info_5 = gisa_df5[['기사 제목', '기사 링크', '기사 내용']]

    '''
    print(graph_info_1)
    print(graph_info_2)
    print(graph_info_3)
    print(graph_info_4)
    '''

    # graph_info_5가 비어있을수도
    graph_info = pd.concat([graph_info_1, graph_info_2, graph_info_3, graph_info_4])

    # graph_info_5가 비어있지 않으면
    if not gisa_df5.empty:
        graph_info = pd.concat([graph_info, graph_info_5])

    #directory = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/김민선/graph_info/' + str(yyyy) + '_' + str(mm)
    directory = './data_storage/graph-info/' + str(yyyy) + '_' + str(mm)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
    graph_info.to_csv(directory + '/' + str(yyyy) + '_' + str(mm) + '_graph-info.csv',
                      encoding='utf-8-sig')  # ''에 csv 생성할 파일 이름 입력

    return gisa_df1, gisa_df2, gisa_df3, gisa_df4, gisa_df5, yyyy, mm