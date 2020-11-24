# -*- coding: utf-8 -*-

import os
import pandas as pd

def find_csv_visual(yyyymm):
  #dir = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/김민선/Apriori'
  dir = './data_storage/Apriori'
  gisa_df1 = pd.DataFrame()
  gisa_df2 = pd.DataFrame()
  yyyy = str(yyyymm)[:4]
  mm = str(yyyymm)[4:]
  if mm[0] == '0':
    mm = mm[1]

  csv_dir = dir + '/' + yyyy + '_' + mm # + '_'
  csv_list = os.listdir(csv_dir)
  csv_list.sort()

  tmp_pd2 = pd.read_csv(csv_dir + '/' + csv_list[0], index_col = 0)
  gisa_df2 = gisa_df2.append(tmp_pd2)
  gisa_df1.reset_index(drop=True, inplace=True)

  return gisa_df2, yyyy, mm

