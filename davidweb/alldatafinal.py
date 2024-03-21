# -*- coding: utf-8 -*-
from django.test import TestCase
import django
import csv,sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'davidweb.settings')
django.setup()

import pandas as pd
from IPython.display import display
from PIL import Image
import sqlite3
import datetime
from pandas import Series, DataFrame
project_dir = "C:\pythongg\davidweb\davidweb"

from mysite import models
base_url = "https://service.taipower.com.tw/data/opendata/apply/file/d007012/001.csv"

models.alldata.objects.all().delete()
models.enddate.objects.all().delete()

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)   

usecol = ["日期","縣市","住宅部門售電量(度)","工業部門售電量(度)"]  #對照輸出英文格式
df_raw = pd.read_csv(base_url, encoding='UTF-8') #UTF-8編碼
df = pd.DataFrame(df_raw)

df.columns = ["date", "country", "self","self per","serve","serve per","farm","farm per","industry","industry per","total","total per"] 
df = df.drop(columns=['self per','serve','serve per','farm','farm per','industry per','total','total per'])
df_filter = df.copy()
df_filter = df_filter[[each >= 201901 for each in df['date']]]
df_filter['self'] = df_filter['self'].str.replace(',', '')
df_filter['self'] = pd.to_numeric(df_filter['self'])
print(df_filter['self'])
df_filter['industry'] = df_filter['industry'].str.replace(',', '')
df_filter['industry'] = pd.to_numeric(df_filter['industry'])
print(df_filter['industry'])
df_filter['date'] = df_filter['date'].astype(str)#將日期欄位轉成str
df_filter['year'] = pd.Series(dtype=int)#新增年欄位
df_filter['month'] = pd.Series(dtype=int)#新增月欄位
df_filter['year'] = df_filter['date'].str[:4].astype(int)#將日期年月分開(年)
df_filter['month'] = df_filter['date'].str[4:7].astype(int)#將日期年月分開(月)
df_filter = df_filter.drop(columns=['date'])#將原先date欄位刪除
#print(df_filter) #各縣市2019~2023的自家用戶以及工業

unit1 = models.enddate()
unit1.year = df_filter.iat[0,3]
unit1.month = df_filter.iat[0,4]
unit1.save()
#----------------------------------北部地區年份2023(春夏秋冬)-------------------------------#
#北部地區
df1 = df_filter.copy()
df1 = df1.loc[(df1['country'] == '台北市') | (df_filter['country'] == '新北市') | (df_filter['country'] == '桃園市') | (df_filter['country'] == '基隆市') | (df_filter['country'] == '新竹市') | (df_filter['country'] == '新竹縣') | (df_filter['country'] == '宜蘭縣')]

#(2023春)
df1_2023 = df1[df1['year'] == 2023]#將df1資料表格中的年份篩選為2022
df1_2023_spring = df1_2023[(df1_2023['month'] == 3) | (df1_2023['month'] == 4) | (df1_2023['month'] == 5)]
df1_2023_spring_new = pd.DataFrame(columns=['area', 'season', 'N_2023_spring_self_avg','N_2023_spring_indusrty_avg']) #新增欄位
df1_2023_spring_self_average = sum(df1_2023_spring['self']) / 3 #算出自家用電平均
df1_2023_spring_industry_average = sum(df1_2023_spring['industry'])/3
df1_2023_spring_new.loc[3] = ['North','Spring', df1_2023_spring_self_average,df1_2023_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二
unit = models.alldata()
unit.year = 2023
unit.area = df1_2023_spring_new.iat[0,0]
unit.season = df1_2023_spring_new.iat[0,1]
unit.self_avg = df1_2023_spring_new.iat[0,2]
unit.industry_avg = df1_2023_spring_new.iat[0,3]
unit.save()

#(2023夏)
df1_2023_summer = df1_2023[(df1_2023['month'] == 6) | (df1_2023['month'] == 7) | (df1_2023['month'] == 8)] 
df1_2023_summer_new = pd.DataFrame(columns=['area', 'season', 'N_2023_summer_self_avg','N_2023_summer_indusrty_avg']) #新增欄位
df1_2023_summer_self_average = sum(df1_2023_summer['self']) / 3 #算出自家用電平均
df1_2023_summer_industry_average = sum(df1_2023_summer['industry'])/3
df1_2023_summer_new.loc[3] = ['North','Summer', df1_2023_summer_self_average,df1_2023_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df1_2023_summer_new.iat[0,0]
unit.season = df1_2023_summer_new.iat[0,1]
unit.self_avg = df1_2023_summer_new.iat[0,2]
unit.industry_avg = df1_2023_summer_new.iat[0,3]
unit.save()

#(2023秋)
df1_2023_autumn = df1_2023[(df1_2023['month'] == 9) | (df1_2023['month'] == 10) | (df1_2023['month'] == 11)]
df1_2023_autumn_new = pd.DataFrame(columns=['area', 'season', 'N_2023_autumn_self_avg','N_2023_autumn_indusrty_avg']) #新增欄位
df1_2023_autumn_self_average = sum(df1_2023_autumn['self']) / 3 #算出自家用電平均
df1_2023_autumn_industry_average = sum(df1_2023_autumn['industry'])/3
df1_2023_autumn_new.loc[3] = ['North','Autumn', df1_2023_autumn_self_average,df1_2023_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df1_2023_autumn_new.iat[0,0]
unit.season = df1_2023_autumn_new.iat[0,1]
unit.self_avg = df1_2023_autumn_new.iat[0,2]
unit.industry_avg = df1_2023_autumn_new.iat[0,3]
unit.save()

#(2023冬)
df1_2023_winter = df1_2023[(df1_2023['month'] == 12) | (df1_2023['month'] == 1) | (df1_2023['month'] == 2)]
df1_2023_winter_new = pd.DataFrame(columns=['area', 'season', 'N_2023_winter_self_avg','N_2023_winter_indusrty_avg']) #新增欄位
df1_2023_winter_self_average = sum(df1_2023_winter['self']) / 3 #算出自家用電平均
df1_2023_winter_industry_average = sum(df1_2023_winter['industry'])/3
df1_2023_winter_new.loc[3] = ['North','Winter', df1_2023_winter_self_average,df1_2023_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df1_2023_winter_new.iat[0,0]
unit.season = df1_2023_winter_new.iat[0,1]
unit.self_avg = df1_2023_winter_new.iat[0,2]
unit.industry_avg = df1_2023_winter_new.iat[0,3]
unit.save()
#----------------------------------北部地區年份2022(春夏秋冬)-------------------------------#
#(2022春)
df1_2022 = df1[df1['year'] == 2022]#將df1資料表格中的年份篩選為2022
df1_2022_spring = df1_2022[(df1_2022['month'] == 3) | (df1_2022['month'] == 4) | (df1_2022['month'] == 5)]
df1_2022_spring_new = pd.DataFrame(columns=['area', 'season', 'N_2022_spring_self_avg','N_2022_spring_indusrty_avg']) #新增欄位
df1_2022_spring_self_average = sum(df1_2022_spring['self']) / 3 #算出自家用電平均
df1_2022_spring_industry_average = sum(df1_2022_spring['industry'])/3
df1_2022_spring_new.loc[3] = ['North','Spring', df1_2022_spring_self_average,df1_2022_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二
unit = models.alldata()
unit.year = 2022
unit.area = df1_2022_spring_new.iat[0,0]
unit.season = df1_2022_spring_new.iat[0,1]
unit.self_avg = df1_2022_spring_new.iat[0,2]
unit.industry_avg = df1_2022_spring_new.iat[0,3]
unit.save()
   
#(2022夏)
df1_2022_summer = df1_2022[(df1_2022['month'] == 6) | (df1_2022['month'] == 7) | (df1_2022['month'] == 8)] 
df1_2022_summer_new = pd.DataFrame(columns=['area', 'season', 'N_2022_summer_self_avg','N_2022_summer_indusrty_avg']) #新增欄位
df1_2022_summer_self_average = sum(df1_2022_summer['self']) / 3 #算出自家用電平均
df1_2022_summer_industry_average = sum(df1_2022_summer['industry'])/3
df1_2022_summer_new.loc[3] = ['North','Summer', df1_2022_summer_self_average,df1_2022_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df1_2022_summer_new.iat[0,0]
unit.season = df1_2022_summer_new.iat[0,1]
unit.self_avg = df1_2022_summer_new.iat[0,2]
unit.industry_avg = df1_2022_summer_new.iat[0,3]
unit.save()
print(df1_2022_summer_new)
#(2022秋)
df1_2022_autumn = df1_2022[(df1_2022['month'] == 9) | (df1_2022['month'] == 10) | (df1_2022['month'] == 11)]
df1_2022_autumn_new = pd.DataFrame(columns=['area', 'season', 'N_2022_autumn_self_avg','N_2022_autumn_indusrty_avg']) #新增欄位
df1_2022_autumn_self_average = sum(df1_2022_autumn['self']) / 3 #算出自家用電平均
df1_2022_autumn_industry_average = sum(df1_2022_autumn['industry'])/3
df1_2022_autumn_new.loc[3] = ['North','Autumn', df1_2022_autumn_self_average,df1_2022_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df1_2022_autumn_new.iat[0,0]
unit.season = df1_2022_autumn_new.iat[0,1]
unit.self_avg = df1_2022_autumn_new.iat[0,2]
unit.industry_avg = df1_2022_autumn_new.iat[0,3]
unit.save()
#print(df1_2022_autumn_new)
#(2022冬)
df1_2022_winter = df1_2022[(df1_2022['month'] == 12) | (df1_2022['month'] == 1) | (df1_2022['month'] == 2)]
df1_2022_winter_new = pd.DataFrame(columns=['area', 'season', 'N_2022_winter_self_avg','N_2022_winter_indusrty_avg']) #新增欄位
df1_2022_winter_self_average = sum(df1_2022_winter['self']) / 3 #算出自家用電平均
df1_2022_winter_industry_average = sum(df1_2022_winter['industry'])/3
df1_2022_winter_new.loc[3] = ['North','Winter', df1_2022_winter_self_average,df1_2022_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df1_2022_winter_new.iat[0,0]
unit.season = df1_2022_winter_new.iat[0,1]
unit.self_avg = df1_2022_winter_new.iat[0,2]
unit.industry_avg = df1_2022_winter_new.iat[0,3]
unit.save()
#print(df1_2022_winter_new)
#----------------------------------北部地區年份2021(春夏秋冬)-------------------------------#
#(2021春)
df1_2021 = df1[df1['year'] == 2021]#將df1資料表格中的年份篩選為2021
df1_2021_spring = df1_2021[(df1_2021['month'] == 3) | (df1_2021['month'] == 4) | (df1_2021['month'] == 5)]
df1_2021_spring_new = pd.DataFrame(columns=['area', 'season', 'N_2021_spring_self_avg','N_2021_spring_indusrty_avg']) #新增欄位
df1_2021_spring_self_average = sum(df1_2021_spring['self']) / 3 #算出自家用電平均
df1_2021_spring_industry_average = sum(df1_2021_spring['industry'])/3
df1_2021_spring_new.loc[3] = ['North','Spring', df1_2021_spring_self_average,df1_2021_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df1_2021_spring_new.iat[0,0]
unit.season = df1_2021_spring_new.iat[0,1]
unit.self_avg = df1_2021_spring_new.iat[0,2]
unit.industry_avg = df1_2021_spring_new.iat[0,3]
unit.save()
#print(df1_2021_spring_new)
#(2021夏)
df1_2021_summer = df1_2021[(df1_2021['month'] == 6) | (df1_2021['month'] == 7) | (df1_2021['month'] == 8)]
df1_2021_summer_new = pd.DataFrame(columns=['area', 'season', 'N_2021_summer_self_avg','N_2021_summer_indusrty_avg']) #新增欄位
df1_2021_summer_self_average = sum(df1_2021_summer['self']) / 3 #算出自家用電平均
df1_2021_summer_industry_average = sum(df1_2021_summer['industry'])/3
df1_2021_summer_new.loc[3] = ['North','Summer', df1_2021_summer_self_average,df1_2021_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df1_2021_summer_new.iat[0,0]
unit.season = df1_2021_summer_new.iat[0,1]
unit.self_avg = df1_2021_summer_new.iat[0,2]
unit.industry_avg = df1_2021_summer_new.iat[0,3]
unit.save()
#print(df1_2021_summer_new) 
#(2021秋)
df1_2021_autumn = df1_2021[(df1_2021['month'] == 9) | (df1_2021['month'] == 10) | (df1_2021['month'] == 11)]
df1_2021_autumn_new = pd.DataFrame(columns=['area', 'season', 'N_2021_autumn_self_avg','N_2021_autumn_indusrty_avg']) #新增欄位
df1_2021_autumn_self_average = sum(df1_2021_autumn['self']) / 3 #算出自家用電平均
df1_2021_autumn_industry_average = sum(df1_2021_autumn['industry'])/3
df1_2021_autumn_new.loc[3] = ['North','Autumn', df1_2021_autumn_self_average,df1_2021_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df1_2021_autumn_new.iat[0,0]
unit.season = df1_2021_autumn_new.iat[0,1]
unit.self_avg = df1_2021_autumn_new.iat[0,2]
unit.industry_avg = df1_2021_autumn_new.iat[0,3]
unit.save()
#print(df1_2021_autumn_new)
#(2021冬)
df1_2021_winter = df1_2021[(df1_2021['month'] == 12) | (df1_2021['month'] == 1) | (df1_2021['month'] == 2)]
df1_2021_winter_new = pd.DataFrame(columns=['area', 'season', 'N_2021_winter_self_avg','N_2021_winter_indusrty_avg']) #新增欄位
df1_2021_winter_self_average = sum(df1_2021_winter['self']) / 3 #算出自家用電平均
df1_2021_winter_industry_average = sum(df1_2021_winter['industry'])/3
df1_2021_winter_new.loc[3] = ['North','Winter', df1_2021_winter_self_average,df1_2021_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df1_2021_winter_new.iat[0,0]
unit.season = df1_2021_winter_new.iat[0,1]
unit.self_avg = df1_2021_winter_new.iat[0,2]
unit.industry_avg = df1_2021_winter_new.iat[0,3]
unit.save()
#print(df1_2021_winter_new)
#----------------------------------北部地區年份2020(春夏秋冬)-------------------------------#
#(2020春)
df1_2020 = df1[df1['year'] == 2020]#將df1資料表格中的年份篩選為2020
df1_2020_spring = df1_2020[(df1_2020['month'] == 3) | (df1_2020['month'] == 4) | (df1_2020['month'] == 5)]
df1_2020_spring_new = pd.DataFrame(columns=['area', 'season', 'N_2020_spring_self_avg','N_2020_spring_indusrty_avg']) #新增欄位
df1_2020_spring_self_average = sum(df1_2020_spring['self']) / 3 #算出自家用電平均
df1_2020_spring_industry_average = sum(df1_2020_spring['industry'])/3
df1_2020_spring_new.loc[3] = ['North','Spring', df1_2020_spring_self_average,df1_2020_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df1_2020_spring_new.iat[0,0]
unit.season = df1_2020_spring_new.iat[0,1]
unit.self_avg = df1_2020_spring_new.iat[0,2]
unit.industry_avg = df1_2020_spring_new.iat[0,3]
unit.save()
#print(df1_2020_spring_new)
#(2020夏)
df1_2020_summer = df1_2020[(df1_2020['month'] == 6) | (df1_2020['month'] == 7) | (df1_2020['month'] == 8)]
df1_2020_summer_new = pd.DataFrame(columns=['area', 'season', 'N_2020_summer_self_avg','N_2020_summer_indusrty_avg']) #新增欄位
df1_2020_summer_self_average = sum(df1_2020_summer['self']) / 3 #算出自家用電平均
df1_2020_summer_industry_average = sum(df1_2020_summer['industry'])/3
df1_2020_summer_new.loc[3] = ['North','Summer', df1_2020_summer_self_average,df1_2020_summer_industry_average]
unit = models.alldata()
unit.year = 2020
unit.area = df1_2020_summer_new.iat[0,0]
unit.season = df1_2020_summer_new.iat[0,1]
unit.self_avg = df1_2020_summer_new.iat[0,2]
unit.industry_avg = df1_2020_summer_new.iat[0,3]
unit.save()
#print(df1_2020_summer_new)
#(2020秋)
df1_2020_autumn = df1_2020[(df1_2020['month'] == 9) | (df1_2020['month'] == 10) | (df1_2020['month'] == 11)]
df1_2020_autumn_new = pd.DataFrame(columns=['area', 'season', 'N_2020_autumn_self_avg','N_2020_autumn_indusrty_avg']) #新增欄位
df1_2020_autumn_self_average = sum(df1_2020_autumn['self']) / 3 #算出自家用電平均
df1_2020_autumn_industry_average = sum(df1_2020_autumn['industry'])/3
df1_2020_autumn_new.loc[3] = ['North','Autumn', df1_2020_autumn_self_average,df1_2020_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df1_2020_autumn_new.iat[0,0]
unit.season = df1_2020_autumn_new.iat[0,1]
unit.self_avg = df1_2020_autumn_new.iat[0,2]
unit.industry_avg = df1_2020_autumn_new.iat[0,3]
unit.save()
#print(df1_2020_autumn_new)
#(2020冬)
df1_2020_winter = df1_2020[(df1_2020['month'] == 12) | (df1_2020['month'] == 1) | (df1_2020['month'] == 2)]
df1_2020_winter_new = pd.DataFrame(columns=['area', 'season', 'N_2020_winter_self_avg','N_2020_winter_indusrty_avg']) #新增欄位
df1_2020_winter_self_average = sum(df1_2020_winter['self']) / 3 #算出自家用電平均
df1_2020_winter_industry_average = sum(df1_2020_winter['industry']) /3
df1_2020_winter_new.loc[3] = ['North','Winter', df1_2020_winter_self_average,df1_2020_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df1_2020_winter_new.iat[0,0]
unit.season = df1_2020_winter_new.iat[0,1]
unit.self_avg = df1_2020_winter_new.iat[0,2]
unit.industry_avg = df1_2020_winter_new.iat[0,3]
unit.save()
#print(df1_2020_winter_new)
#----------------------------------北部地區年份2019(春夏秋冬)-------------------------------#
#(2019春)
df1_2019 = df1[df1['year'] == 2019]#將df1資料表格中的年份篩選為2022
df1_2019_spring = df1_2019[(df1_2019['month'] == 3) | (df1_2019['month'] == 4) | (df1_2019['month'] == 5)]
df1_2019_spring_new = pd.DataFrame(columns=['area', 'season', 'N_2019_spring_self_avg','N_2019_spring_indusrty_avg']) #新增欄位
df1_2019_spring_self_average = sum(df1_2019_spring['self']) / 3 #算出自家用電平均
df1_2019_spring_industry_average = sum(df1_2019_spring['industry']) /3
df1_2019_spring_new.loc[3] = ['North','Spring', df1_2019_spring_self_average,df1_2019_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df1_2019_spring_new.iat[0,0]
unit.season = df1_2019_spring_new.iat[0,1]
unit.self_avg = df1_2019_spring_new.iat[0,2]
unit.industry_avg = df1_2019_spring_new.iat[0,3]
unit.save()
#print(df1_2019_spring_new)
#(2019夏)
df1_2019_summer = df1_2019[(df1_2019['month'] == 6) | (df1_2019['month'] == 7) | (df1_2019['month'] == 8)]
df1_2019_summer_new = pd.DataFrame(columns=['area', 'season', 'N_2019_summer_self_avg','N_2019_summer_indusrty_avg']) #新增欄位
df1_2019_summer_self_average = sum(df1_2019_summer['self']) / 3 #算出自家用電平均
df1_2019_summer_industry_average = sum(df1_2019_summer['industry']) /3
df1_2019_summer_new.loc[3] = ['North','Summer', df1_2019_summer_self_average,df1_2019_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df1_2019_summer_new.iat[0,0]
unit.season = df1_2019_summer_new.iat[0,1]
unit.self_avg = df1_2019_summer_new.iat[0,2]
unit.industry_avg = df1_2019_summer_new.iat[0,3]
unit.save()
#print(df1_2019_summer_new)
#(2019秋)
df1_2019_autumn = df1_2019[(df1_2019['month'] == 9) | (df1_2019['month'] == 10) | (df1_2019['month'] == 11)]
df1_2019_autumn_new = pd.DataFrame(columns=['area', 'season', 'N_2019_autumn_self_avg','N_2019_autumn_indusrty_avg']) #新增欄位
df1_2019_autumn_self_average = sum(df1_2019_autumn['self']) / 3 #算出自家用電平均
df1_2019_autumn_industry_average = sum(df1_2019_autumn['industry']) /3
df1_2019_autumn_new.loc[3] = ['North','Autumn', df1_2019_autumn_self_average,df1_2019_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df1_2019_autumn_new.iat[0,0]
unit.season = df1_2019_autumn_new.iat[0,1]
unit.self_avg = df1_2019_autumn_new.iat[0,2]
unit.industry_avg = df1_2019_autumn_new.iat[0,3]
unit.save()
#print(df1_2019_autumn_new)
#(2019冬)
df1_2019_winter = df1_2019[(df1_2019['month'] == 12) | (df1_2019['month'] == 1) | (df1_2019['month'] == 2)] 
df1_2019_winter_new = pd.DataFrame(columns=['area', 'season', 'N_2019_winter_self_avg','N_2019_winter_indusrty_avg']) #新增欄位
df1_2019_winter_self_average = sum(df1_2019_winter['self']) / 3 #算出自家用電平均
df1_2019_winter_industry_average = sum(df1_2019_winter['industry']) /3
df1_2019_winter_new.loc[3] = ['North','Winter', df1_2019_winter_self_average,df1_2019_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df1_2019_winter_new.iat[0,0]
unit.season = df1_2019_winter_new.iat[0,1]
unit.self_avg = df1_2019_winter_new.iat[0,2]
unit.industry_avg = df1_2019_winter_new.iat[0,3]
unit.save()
#print(df1_2019_winter_new)




#中部地區
df2 = df_filter.copy()
df2 = df_filter.loc[(df_filter['country'] == '台中市') | (df_filter['country'] == '苗栗縣') | (df_filter['country'] == '彰化縣') | (df_filter['country'] == '南投縣') | (df_filter['country'] == '雲林縣')]
#----------------------------------中部地區年份2023(春夏秋冬)-------------------------------#
#(2023春)
df2_2023 = df2[df2['year'] == 2023]#將df2資料表格中的年份篩選為2023
df2_2023_spring = df2_2023[(df2_2023['month'] == 3) | (df2_2023['month'] == 4) | (df2_2023['month'] == 5)]
df2_2023_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2023_spring_self_avg','M_2023_spring_indusrty_avg']) #新增欄位
df2_2023_spring_self_average = sum(df2_2023_spring['self']) / 3 #算出自家用電平均
df2_2023_spring_industry_average = sum(df2_2023_spring['industry'])/3
df2_2023_spring_new.loc[3] = ['Middle','Spring', df2_2023_spring_self_average,df2_2023_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df2_2023_spring_new.iat[0,0]
unit.season = df2_2023_spring_new.iat[0,1]
unit.self_avg = df2_2023_spring_new.iat[0,2]
unit.industry_avg = df2_2023_spring_new.iat[0,3]
unit.save()

#(2023夏)
df2_2023_summer = df2_2023[(df2_2023['month'] == 6) | (df2_2023['month'] == 7) | (df2_2023['month'] == 8)]
df2_2023_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2023_summer_self_avg','M_2023_summer_indusrty_avg']) #新增欄位
df2_2023_summer_self_average = sum(df2_2023_summer['self']) / 3 #算出自家用電平均
df2_2023_summer_industry_average = sum(df2_2023_summer['industry'])/3
df2_2023_summer_new.loc[3] = ['Middle','Summer', df2_2023_summer_self_average,df2_2023_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df2_2023_summer_new.iat[0,0]
unit.season = df2_2023_summer_new.iat[0,1]
unit.self_avg = df2_2023_summer_new.iat[0,2]
unit.industry_avg = df2_2023_summer_new.iat[0,3]
unit.save()

#(2023秋)
df2_2023_autumn = df2_2023[(df2_2023['month'] == 9) | (df2_2023['month'] == 10) | (df2_2023['month'] == 11)]
df2_2023_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2023_autumn_self_avg','M_2023_autumn_indusrty_avg']) #新增欄位
df2_2023_autumn_self_average = sum(df2_2023_autumn['self']) / 3 #算出自家用電平均
df2_2023_autumn_industry_average = sum(df2_2023_autumn['industry'])/3
df2_2023_autumn_new.loc[3] = ['Middle','Autumn', df2_2023_autumn_self_average,df2_2023_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df2_2023_autumn_new.iat[0,0]
unit.season = df2_2023_autumn_new.iat[0,1]
unit.self_avg = df2_2023_autumn_new.iat[0,2]
unit.industry_avg = df2_2023_autumn_new.iat[0,3]
unit.save()

#(2023冬)
df2_2023_winter = df2_2023[(df2_2023['month'] == 12) | (df2_2023['month'] == 1) | (df2_2023['month'] == 2)]
df2_2023_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2023_winter_self_avg','M_2023_winter_indusrty_avg']) #新增欄位
df2_2023_winter_self_average = sum(df2_2023_winter['self']) / 3 #算出自家用電平均
df2_2023_winter_industry_average = sum(df2_2023_winter['industry'])/3
df2_2023_winter_new.loc[3] = ['Middle','Winter', df2_2023_winter_self_average,df2_2023_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df2_2023_winter_new.iat[0,0]
unit.season = df2_2023_winter_new.iat[0,1]
unit.self_avg = df2_2023_winter_new.iat[0,2]
unit.industry_avg = df2_2023_winter_new.iat[0,3]
unit.save()

#----------------------------------中部地區年份2022(春夏秋冬)-------------------------------#
#(2022春)
df2_2022 = df2[df2['year'] == 2022]#將df2資料表格中的年份篩選為2022
df2_2022_spring = df2_2022[(df2_2022['month'] == 3) | (df2_2022['month'] == 4) | (df2_2022['month'] == 5)]
df2_2022_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2022_spring_self_avg','M_2022_spring_indusrty_avg']) #新增欄位
df2_2022_spring_self_average = sum(df2_2022_spring['self']) / 3 #算出自家用電平均
df2_2022_spring_industry_average = sum(df2_2022_spring['industry'])/3
df2_2022_spring_new.loc[3] = ['Middle','Spring', df2_2022_spring_self_average,df2_2022_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df2_2022_spring_new.iat[0,0]
unit.season = df2_2022_spring_new.iat[0,1]
unit.self_avg = df2_2022_spring_new.iat[0,2]
unit.industry_avg = df2_2022_spring_new.iat[0,3]
unit.save()
#print(df2_2022_spring_new)
#(2022夏)
df2_2022_summer = df2_2022[(df2_2022['month'] == 6) | (df2_2022['month'] == 7) | (df2_2022['month'] == 8)]
df2_2022_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2022_summer_self_avg','M_2022_summer_indusrty_avg']) #新增欄位
df2_2022_summer_self_average = sum(df2_2022_summer['self']) / 3 #算出自家用電平均
df2_2022_summer_industry_average = sum(df2_2022_summer['industry'])/3
df2_2022_summer_new.loc[3] = ['Middle','Summer', df2_2022_summer_self_average,df2_2022_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df2_2022_summer_new.iat[0,0]
unit.season = df2_2022_summer_new.iat[0,1]
unit.self_avg = df2_2022_summer_new.iat[0,2]
unit.industry_avg = df2_2022_summer_new.iat[0,3]
unit.save()
#print(df2_2022_summer_new)
#(2022秋)
df2_2022_autumn = df2_2022[(df2_2022['month'] == 9) | (df2_2022['month'] == 10) | (df2_2022['month'] == 11)]
df2_2022_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2022_autumn_self_avg','M_2022_autumn_indusrty_avg']) #新增欄位
df2_2022_autumn_self_average = sum(df2_2022_autumn['self']) / 3 #算出自家用電平均
df2_2022_autumn_industry_average = sum(df2_2022_autumn['industry'])/3
df2_2022_autumn_new.loc[3] = ['Middle','Autumn', df2_2022_autumn_self_average,df2_2022_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df2_2022_autumn_new.iat[0,0]
unit.season = df2_2022_autumn_new.iat[0,1]
unit.self_avg = df2_2022_autumn_new.iat[0,2]
unit.industry_avg = df2_2022_autumn_new.iat[0,3]
unit.save()
#print(df2_2022_autumn_new)
#(2022冬)
df2_2022_winter = df2_2022[(df2_2022['month'] == 12) | (df2_2022['month'] == 1) | (df2_2022['month'] == 2)]
df2_2022_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2022_winter_self_avg','M_2022_winter_indusrty_avg']) #新增欄位
df2_2022_winter_self_average = sum(df2_2022_winter['self']) / 3 #算出自家用電平均
df2_2022_winter_industry_average = sum(df2_2022_winter['industry'])/3
df2_2022_winter_new.loc[3] = ['Middle','Winter', df2_2022_winter_self_average,df2_2022_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df2_2022_winter_new.iat[0,0]
unit.season = df2_2022_winter_new.iat[0,1]
unit.self_avg = df2_2022_winter_new.iat[0,2]
unit.industry_avg = df2_2022_winter_new.iat[0,3]
unit.save()
#print(df2_2022_winter_new)
#----------------------------------中部地區年份2021(春夏秋冬)-------------------------------#
#(2021春)
df2_2021 = df2[df2['year'] == 2021]#將df2資料表格中的年份篩選為2022
df2_2021_spring = df2_2021[(df2_2021['month'] == 3) | (df2_2021['month'] == 4) | (df2_2021['month'] == 5)]
df2_2021_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2021_spring_self_avg','M_2021_spring_indusrty_avg']) #新增欄位
df2_2021_spring_self_average = sum(df2_2021_spring['self']) / 3 #算出自家用電平均
df2_2021_spring_industry_average = sum(df2_2021_spring['industry'])/3
df2_2021_spring_new.loc[3] = ['Middle','Spring', df2_2021_spring_self_average,df2_2021_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df2_2021_spring_new.iat[0,0]
unit.season = df2_2021_spring_new.iat[0,1]
unit.self_avg = df2_2021_spring_new.iat[0,2]
unit.industry_avg = df2_2021_spring_new.iat[0,3]
unit.save()
#print(df2_2021_spring_new)
#(2021夏)
df2_2021_summer = df2_2021[(df2_2021['month'] == 6) | (df2_2021['month'] == 7) | (df2_2021['month'] == 8)]
df2_2021_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2021_summer_self_avg','M_2021_summer_indusrty_avg']) #新增欄位
df2_2021_summer_self_average = sum(df2_2021_summer['self']) / 3 #算出自家用電平均
df2_2021_summer_industry_average = sum(df2_2021_summer['industry'])/3
df2_2021_summer_new.loc[3] = ['Middle','Summer', df2_2021_summer_self_average,df2_2021_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df2_2021_summer_new.iat[0,0]
unit.season = df2_2021_summer_new.iat[0,1]
unit.self_avg = df2_2021_summer_new.iat[0,2]
unit.industry_avg = df2_2021_summer_new.iat[0,3]
unit.save()
#print(df2_2021_summer_new)
#(2021秋)
df2_2021_autumn = df2_2021[(df2_2021['month'] == 9) | (df2_2021['month'] == 10) | (df2_2021['month'] == 11)] 
df2_2021_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2021_autumn_self_avg','M_2021_autumn_indusrty_avg']) #新增欄位
df2_2021_autumn_self_average = sum(df2_2021_autumn['self']) / 3 #算出自家用電平均
df2_2021_autumn_industry_average = sum(df2_2021_autumn['industry'])/3
df2_2021_autumn_new.loc[3] = ['Middle','Autumn', df2_2021_autumn_self_average,df2_2021_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df2_2021_autumn_new.iat[0,0]
unit.season = df2_2021_autumn_new.iat[0,1]
unit.self_avg = df2_2021_autumn_new.iat[0,2]
unit.industry_avg = df2_2021_autumn_new.iat[0,3]
unit.save()
#print(df2_2021_autumn_new)
#(2021冬)
df2_2021_winter = df2_2021[(df2_2021['month'] == 12) | (df2_2021['month'] == 1) | (df2_2021['month'] == 2)]
df2_2021_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2021_winter_self_avg','M_2021_winter_indusrty_avg']) #新增欄位
df2_2021_winter_self_average = sum(df2_2021_winter['self']) / 3 #算出自家用電平均
df2_2021_winter_industry_average = sum(df2_2021_winter['industry'])/3
df2_2021_winter_new.loc[3] = ['Middle','Winter', df2_2021_winter_self_average,df2_2021_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df2_2021_winter_new.iat[0,0]
unit.season = df2_2021_winter_new.iat[0,1]
unit.self_avg = df2_2021_winter_new.iat[0,2]
unit.industry_avg = df2_2021_winter_new.iat[0,3]
unit.save()
#print(df2_2021_winter_new)

#----------------------------------中部地區年份2020(春夏秋冬)-------------------------------#
#(2020春)
df2_2020 = df2[df2['year'] == 2020]#將df2資料表格中的年份篩選為2020
df2_2020_spring = df2_2020[(df2_2020['month'] == 3) | (df2_2020['month'] == 4) | (df2_2020['month'] == 5)]
df2_2020_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2020_spring_self_avg','M_2020_spring_indusrty_avg']) #新增欄位
df2_2020_spring_self_average = sum(df2_2020_spring['self']) / 3 #算出自家用電平均
df2_2020_spring_industry_average = sum(df2_2020_spring['industry'])/3
df2_2020_spring_new.loc[3] = ['Middle','Spring', df2_2020_spring_self_average,df2_2020_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df2_2020_spring_new.iat[0,0]
unit.season = df2_2020_spring_new.iat[0,1]
unit.self_avg = df2_2020_spring_new.iat[0,2]
unit.industry_avg = df2_2020_spring_new.iat[0,3]
unit.save()
#print(df2_2020_spring_new)
#(2020夏)
df2_2020_summer = df2_2020[(df2_2020['month'] == 6) | (df2_2020['month'] == 7) | (df2_2020['month'] == 8)]
df2_2020_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2020_summer_self_avg','M_2020_summer_indusrty_avg']) #新增欄位
df2_2020_summer_self_average = sum(df2_2020_summer['self']) / 3 #算出自家用電平均
df2_2020_summer_industry_average = sum(df2_2020_summer['industry'])/3
df2_2020_summer_new.loc[3] = ['Middle','Summer', df2_2020_summer_self_average,df2_2020_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df2_2020_summer_new.iat[0,0]
unit.season = df2_2020_summer_new.iat[0,1]
unit.self_avg = df2_2020_summer_new.iat[0,2]
unit.industry_avg = df2_2020_summer_new.iat[0,3]
unit.save()
#print(df2_2020_summer_new)
#(2020秋)
df2_2020_autumn = df2_2020[(df2_2020['month'] == 9) | (df2_2020['month'] == 10) | (df2_2020['month'] == 11)]
df2_2020_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2020_autumn_self_avg','M_2020_autumn_indusrty_avg']) #新增欄位
df2_2020_autumn_self_average = sum(df2_2020_autumn['self']) / 3 #算出自家用電平均
df2_2020_autumn_industry_average = sum(df2_2020_autumn['industry'])/3
df2_2020_autumn_new.loc[3] = ['Middle','Autumn', df2_2020_autumn_self_average,df2_2020_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df2_2020_autumn_new.iat[0,0]
unit.season = df2_2020_autumn_new.iat[0,1]
unit.self_avg = df2_2020_autumn_new.iat[0,2]
unit.industry_avg = df2_2020_autumn_new.iat[0,3]
unit.save()
#print(df2_2020_autumn_new)
#(2020冬)
df2_2020_winter = df2_2020[(df2_2020['month'] == 12) | (df2_2020['month'] == 1) | (df2_2020['month'] == 2)]
df2_2020_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2020_winter_self_avg','M_2020_winter_indusrty_avg']) #新增欄位
df2_2020_winter_self_average = sum(df2_2020_winter['self']) / 3 #算出自家用電平均
df2_2020_winter_industry_average = sum(df2_2020_winter['industry'])/3
df2_2020_winter_new.loc[3] = ['Middle','Winter', df2_2020_winter_self_average,df2_2020_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df2_2020_winter_new.iat[0,0]
unit.season = df2_2020_winter_new.iat[0,1]
unit.self_avg = df2_2020_winter_new.iat[0,2]
unit.industry_avg = df2_2020_winter_new.iat[0,3]
unit.save()
#print(df2_2020_winter_new) 

#----------------------------------中部地區年份2019(春夏秋冬)-------------------------------#
#(2019春)
df2_2019 = df2[df2['year'] == 2019]#將df2資料表格中的年份篩選為2022
df2_2019_spring = df2_2019[(df2_2019['month'] == 3) | (df2_2019['month'] == 4) | (df2_2019['month'] == 5)]
df2_2019_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2019_spring_self_avg','M_2019_spring_indusrty_avg']) #新增欄位
df2_2019_spring_self_average = sum(df2_2019_spring['self'])/3 #算出自家用電平均
df2_2019_spring_industry_average = sum(df2_2019_spring['industry'])/3
df2_2019_spring_new.loc[3] = ['Middle','Spring', df2_2019_spring_self_average,df2_2019_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df2_2019_spring_new.iat[0,0]
unit.season = df2_2019_spring_new.iat[0,1]
unit.self_avg = df2_2019_spring_new.iat[0,2]
unit.industry_avg = df2_2019_spring_new.iat[0,3]
unit.save()
#print(df2_2019_spring_new) 
#(2019夏)
df2_2019_summer = df2_2019[(df2_2019['month'] == 6) | (df2_2019['month'] == 7) | (df2_2019['month'] == 8)]
df2_2019_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2019_summer_self_avg','M_2019_summer_indusrty_avg']) #新增欄位
df2_2019_summer_self_average = sum(df2_2019_summer['self']) / 3 #算出自家用電平均
df2_2019_summer_industry_average = sum(df2_2019_summer['industry'])/3
df2_2019_summer_new.loc[3] = ['Middle','Summer', df2_2019_summer_self_average,df2_2019_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df2_2019_summer_new.iat[0,0]
unit.season = df2_2019_summer_new.iat[0,1]
unit.self_avg = df2_2019_summer_new.iat[0,2]
unit.industry_avg = df2_2019_summer_new.iat[0,3]
unit.save()
#print(df2_2019_summer_new)  
#(2019秋)
df2_2019_autumn = df2_2019[(df2_2019['month'] == 9) | (df2_2019['month'] == 10) | (df2_2019['month'] == 11)] 
df2_2019_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2019_autumn_self_avg','M_2019_autumn_indusrty_avg']) #新增欄位
df2_2019_autumn_self_average = sum(df2_2019_autumn['self']) / 3 #算出自家用電平均
df2_2019_autumn_industry_average = sum(df2_2019_autumn['industry'])/3
df2_2019_autumn_new.loc[3] = ['Middle','Autumn', df2_2019_autumn_self_average,df2_2019_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df2_2019_autumn_new.iat[0,0]
unit.season = df2_2019_autumn_new.iat[0,1]
unit.self_avg = df2_2019_autumn_new.iat[0,2]
unit.industry_avg = df2_2019_autumn_new.iat[0,3]
unit.save()
#print(df2_2019_autumn_new)  
#(2019冬)
df2_2019_winter = df2_2019[(df2_2019['month'] == 12) | (df2_2019['month'] == 1) | (df2_2019['month'] == 2)] 
df2_2019_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2019_winter_self_avg','M_2019_winter_indusrty_avg']) #新增欄位
df2_2019_winter_self_average = sum(df2_2019_winter['self']) / 3 #算出自家用電平均
df2_2019_winter_industry_average = sum(df2_2019_winter['industry'])/3
df2_2019_winter_new.loc[3] = ['Middle','Winter', df2_2019_winter_self_average,df2_2019_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df2_2019_winter_new.iat[0,0]
unit.season = df2_2019_winter_new.iat[0,1]
unit.self_avg = df2_2019_winter_new.iat[0,2]
unit.industry_avg = df2_2019_winter_new.iat[0,3]
unit.save()
#print(df2_2019_winter_new)  

#南部地區
df3 = df_filter.copy()
df3 = df_filter.loc[(df_filter['country'] == '高雄市') | (df_filter['country'] == '台南市') | (df_filter['country'] == '嘉義縣') | (df_filter['country'] == '屏東縣') | (df_filter['country'] == '澎湖縣')]
#----------------------------------南部地區年份2023(春夏秋冬)-------------------------------#
#(2023春)
df3_2023 = df3[df3['year'] == 2023]#將df3資料表格中的年份篩選為2023
df3_2023_spring = df3_2023[(df3_2023['month'] == 3) | (df3_2023['month'] == 4) | (df3_2023['month'] == 5)]
df3_2023_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2023_spring_self_avg','M_2023_spring_indusrty_avg']) #新增欄位
df3_2023_spring_self_average = sum(df3_2023_spring['self']) / 3 #算出自家用電平均
df3_2023_spring_industry_average = sum(df3_2023_spring['industry'])/3
df3_2023_spring_new.loc[3] = ['South','Spring', df3_2023_spring_self_average,df3_2023_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df3_2023_spring_new.iat[0,0]
unit.season = df3_2023_spring_new.iat[0,1]
unit.self_avg = df3_2023_spring_new.iat[0,2]
unit.industry_avg = df3_2023_spring_new.iat[0,3]
unit.save()

#(2023夏)
df3_2023_summer = df3_2023[(df3_2023['month'] == 6) | (df3_2023['month'] == 7) | (df3_2023['month'] == 8)]
df3_2023_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2023_summer_self_avg','M_2023_summer_indusrty_avg']) #新增欄位
df3_2023_summer_self_average = sum(df3_2023_summer['self']) / 3 #算出自家用電平均
df3_2023_summer_industry_average = sum(df3_2023_summer['industry'])/3
df3_2023_summer_new.loc[3] = ['South','Summer', df3_2023_summer_self_average,df3_2023_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df3_2023_summer_new.iat[0,0]
unit.season = df3_2023_summer_new.iat[0,1]
unit.self_avg = df3_2023_summer_new.iat[0,2]
unit.industry_avg = df3_2023_summer_new.iat[0,3]
unit.save()

#(2023秋)
df3_2023_autumn = df3_2023[(df3_2023['month'] == 9) | (df3_2023['month'] == 10) | (df3_2023['month'] == 11)]
df3_2023_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2023_autumn_self_avg','M_2023_autumn_indusrty_avg']) #新增欄位
df3_2023_autumn_self_average = sum(df3_2023_autumn['self']) / 3 #算出自家用電平均
df3_2023_autumn_industry_average = sum(df3_2023_autumn['industry'])/3
df3_2023_autumn_new.loc[3] = ['South','Autumn', df3_2023_autumn_self_average,df3_2023_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df3_2023_autumn_new.iat[0,0]
unit.season = df3_2023_autumn_new.iat[0,1]
unit.self_avg = df3_2023_autumn_new.iat[0,2]
unit.industry_avg = df3_2023_autumn_new.iat[0,3]
unit.save()

#(2023冬)
df3_2023_winter = df3_2023[(df3_2023['month'] == 12) | (df3_2023['month'] == 1) | (df3_2023['month'] == 2)] 
df3_2023_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2023_winter_self_avg','M_2023_winter_indusrty_avg']) #新增欄位
df3_2023_winter_self_average = sum(df3_2023_winter['self']) / 3 #算出自家用電平均
df3_2023_winter_industry_average = sum(df3_2023_winter['industry'])/3
df3_2023_winter_new.loc[3] = ['South','Winter', df3_2023_winter_self_average,df3_2023_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df3_2023_winter_new.iat[0,0]
unit.season = df3_2023_winter_new.iat[0,1]
unit.self_avg = df3_2023_winter_new.iat[0,2]
unit.industry_avg = df3_2023_winter_new.iat[0,3]
unit.save()

#----------------------------------南部地區年份2022(春夏秋冬)-------------------------------#
#(2022春)
df3_2022 = df3[df3['year'] == 2022]#將df3資料表格中的年份篩選為2022
df3_2022_spring = df3_2022[(df3_2022['month'] == 3) | (df3_2022['month'] == 4) | (df3_2022['month'] == 5)]
df3_2022_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2022_spring_self_avg','M_2022_spring_indusrty_avg']) #新增欄位
df3_2022_spring_self_average = sum(df3_2022_spring['self']) / 3 #算出自家用電平均
df3_2022_spring_industry_average = sum(df3_2022_spring['industry'])/3
df3_2022_spring_new.loc[3] = ['South','Spring', df3_2022_spring_self_average,df3_2022_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df3_2022_spring_new.iat[0,0]
unit.season = df3_2022_spring_new.iat[0,1]
unit.self_avg = df3_2022_spring_new.iat[0,2]
unit.industry_avg = df3_2022_spring_new.iat[0,3]
unit.save()
#print(df3_2022_spring_new) 
#(2022夏)
df3_2022_summer = df3_2022[(df3_2022['month'] == 6) | (df3_2022['month'] == 7) | (df3_2022['month'] == 8)]
df3_2022_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2022_summer_self_avg','M_2022_summer_indusrty_avg']) #新增欄位
df3_2022_summer_self_average = sum(df3_2022_summer['self']) / 3 #算出自家用電平均
df3_2022_summer_industry_average = sum(df3_2022_summer['industry'])/3
df3_2022_summer_new.loc[3] = ['South','Summer', df3_2022_summer_self_average,df3_2022_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df3_2022_summer_new.iat[0,0]
unit.season = df3_2022_summer_new.iat[0,1]
unit.self_avg = df3_2022_summer_new.iat[0,2]
unit.industry_avg = df3_2022_summer_new.iat[0,3]
unit.save()
#print(df3_2022_summer_new)  
#(2022秋)
df3_2022_autumn = df3_2022[(df3_2022['month'] == 9) | (df3_2022['month'] == 10) | (df3_2022['month'] == 11)]
df3_2022_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2022_autumn_self_avg','M_2022_autumn_indusrty_avg']) #新增欄位
df3_2022_autumn_self_average = sum(df3_2022_autumn['self']) / 3 #算出自家用電平均
df3_2022_autumn_industry_average = sum(df3_2022_autumn['industry'])/3
df3_2022_autumn_new.loc[3] = ['South','Autumn', df3_2022_autumn_self_average,df3_2022_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df3_2022_autumn_new.iat[0,0]
unit.season = df3_2022_autumn_new.iat[0,1]
unit.self_avg = df3_2022_autumn_new.iat[0,2]
unit.industry_avg = df3_2022_autumn_new.iat[0,3]
unit.save()
#print(df3_2022_autumn_new)  
#(2022冬)
df3_2022_winter = df3_2022[(df3_2022['month'] == 12) | (df3_2022['month'] == 1) | (df3_2022['month'] == 2)] 
df3_2022_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2022_winter_self_avg','M_2022_winter_indusrty_avg']) #新增欄位
df3_2022_winter_self_average = sum(df3_2022_winter['self']) / 3 #算出自家用電平均
df3_2022_winter_industry_average = sum(df3_2022_winter['industry'])/3
df3_2022_winter_new.loc[3] = ['South','Winter', df3_2022_winter_self_average,df3_2022_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df3_2022_winter_new.iat[0,0]
unit.season = df3_2022_winter_new.iat[0,1]
unit.self_avg = df3_2022_winter_new.iat[0,2]
unit.industry_avg = df3_2022_winter_new.iat[0,3]
unit.save()
#print(df3_2022_winter_new) 
#----------------------------------南部地區年份2021(春夏秋冬)-------------------------------#
#(2021春)
df3_2021 = df3[df3['year'] == 2021]#將df3資料表格中的年份篩選為2021
df3_2021_spring = df3_2021[(df3_2021['month'] == 3) | (df3_2021['month'] == 4) | (df3_2021['month'] == 5)] 
df3_2021_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2021_spring_self_avg','M_2021_spring_indusrty_avg']) #新增欄位
df3_2021_spring_self_average = sum(df3_2021_spring['self']) / 3 #算出自家用電平均
df3_2021_spring_industry_average = sum(df3_2021_spring['industry'])/3
df3_2021_spring_new.loc[3] = ['South','Spring', df3_2021_spring_self_average,df3_2021_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df3_2021_spring_new.iat[0,0]
unit.season = df3_2021_spring_new.iat[0,1]
unit.self_avg = df3_2021_spring_new.iat[0,2]
unit.industry_avg = df3_2021_spring_new.iat[0,3]
unit.save()
#print(df3_2021_spring_new) 
#(2021夏)
df3_2021_summer = df3_2021[(df3_2021['month'] == 6) | (df3_2021['month'] == 7) | (df3_2021['month'] == 8)]
df3_2021_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2021_summer_self_avg','M_2021_summer_indusrty_avg']) #新增欄位
df3_2021_summer_self_average = sum(df3_2021_summer['self']) / 3 #算出自家用電平均
df3_2021_summer_industry_average = sum(df3_2021_summer['industry'])/3
df3_2021_summer_new.loc[3] = ['South','Summer', df3_2021_summer_self_average,df3_2021_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df3_2021_summer_new.iat[0,0]
unit.season = df3_2021_summer_new.iat[0,1]
unit.self_avg = df3_2021_summer_new.iat[0,2]
unit.industry_avg = df3_2021_summer_new.iat[0,3]
unit.save()
#print(df3_2021_summer_new) 
#(2021秋)
df3_2021_autumn = df3_2021[(df3_2021['month'] == 9) | (df3_2021['month'] == 10) | (df3_2021['month'] == 11)]
df3_2021_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2021_autumn_self_avg','M_2021_autumn_indusrty_avg']) #新增欄位
df3_2021_autumn_self_average = sum(df3_2021_autumn['self']) / 3 #算出自家用電平均
df3_2021_autumn_industry_average = sum(df3_2021_autumn['industry'])/3
df3_2021_autumn_new.loc[3] = ['South','Autumn', df3_2021_autumn_self_average,df3_2021_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df3_2021_autumn_new.iat[0,0]
unit.season = df3_2021_autumn_new.iat[0,1]
unit.self_avg = df3_2021_autumn_new.iat[0,2]
unit.industry_avg = df3_2021_autumn_new.iat[0,3]
unit.save()
#print(df3_2021_autumn_new) 
#(2021冬)
df3_2021_winter = df3_2021[(df3_2021['month'] == 12) | (df3_2021['month'] == 1) | (df3_2021['month'] == 2)] 
df3_2021_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2021_winter_self_avg','M_2021_winter_indusrty_avg']) #新增欄位
df3_2021_winter_self_average = sum(df3_2021_winter['self']) / 3 #算出自家用電平均
df3_2021_winter_industry_average = sum(df3_2021_winter['industry'])/3
df3_2021_winter_new.loc[3] = ['South','Winter', df3_2021_winter_self_average,df3_2021_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df3_2021_winter_new.iat[0,0]
unit.season = df3_2021_winter_new.iat[0,1]
unit.self_avg = df3_2021_winter_new.iat[0,2]
unit.industry_avg = df3_2021_winter_new.iat[0,3]
unit.save()
#print(df3_2021_winter_new) 
#----------------------------------南部地區年份2020(春夏秋冬)-------------------------------#
#(2020春)
df3_2020 = df3[df3['year'] == 2020]#將df3資料表格中的年份篩選為2022
df3_2020_spring = df3_2020[(df3_2020['month'] == 3) | (df3_2020['month'] == 4) | (df3_2020['month'] == 5)]
df3_2020_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2020_spring_self_avg','M_2020_spring_indusrty_avg']) #新增欄位
df3_2020_spring_self_average = sum(df3_2020_spring['self']) / 3 #算出自家用電平均
df3_2020_spring_industry_average = sum(df3_2020_spring['industry'])/3
df3_2020_spring_new.loc[3] = ['South','Spring', df3_2020_spring_self_average,df3_2020_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df3_2020_spring_new.iat[0,0]
unit.season = df3_2020_spring_new.iat[0,1]
unit.self_avg = df3_2020_spring_new.iat[0,2]
unit.industry_avg = df3_2020_spring_new.iat[0,3]
unit.save()
#print(df3_2020_spring_new)  
#(2020夏)
df3_2020_summer = df3_2020[(df3_2020['month'] == 6) | (df3_2020['month'] == 7) | (df3_2020['month'] == 8)]
df3_2020_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2020_summer_self_avg','M_2020_summer_indusrty_avg']) #新增欄位
df3_2020_summer_self_average = sum(df3_2020_summer['self']) / 3 #算出自家用電平均
df3_2020_summer_industry_average = sum(df3_2020_summer['industry'])/3
df3_2020_summer_new.loc[3] = ['South','Summer', df3_2020_summer_self_average,df3_2020_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df3_2020_summer_new.iat[0,0]
unit.season = df3_2020_summer_new.iat[0,1]
unit.self_avg = df3_2020_summer_new.iat[0,2]
unit.industry_avg = df3_2020_summer_new.iat[0,3]
unit.save()
#print(df3_2020_summer_new)  
#(2020秋)
df3_2020_autumn = df3_2020[(df3_2020['month'] == 9) | (df3_2020['month'] == 10) | (df3_2020['month'] == 11)]
df3_2020_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2020_autumn_self_avg','M_2020_autumn_indusrty_avg']) #新增欄位
df3_2020_autumn_self_average = sum(df3_2020_autumn['self']) / 3 #算出自家用電平均
df3_2020_autumn_industry_average = sum(df3_2020_autumn['industry'])/3
df3_2020_autumn_new.loc[3] = ['South','Autumn', df3_2020_autumn_self_average,df3_2020_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df3_2020_autumn_new.iat[0,0]
unit.season = df3_2020_autumn_new.iat[0,1]
unit.self_avg = df3_2020_autumn_new.iat[0,2]
unit.industry_avg = df3_2020_autumn_new.iat[0,3]
unit.save()
#print(df3_2020_autumn_new)  
#(2020冬)
df3_2020_winter = df3_2020[(df3_2020['month'] == 12) | (df3_2020['month'] == 1) | (df3_2020['month'] == 2)] 
df3_2020_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2020_winter_self_avg','M_2020_winter_indusrty_avg']) #新增欄位
df3_2020_winter_self_average = sum(df3_2020_winter['self']) / 3 #算出自家用電平均
df3_2020_winter_industry_average = sum(df3_2020_winter['industry'])/3
df3_2020_winter_new.loc[3] = ['South','Winter', df3_2020_winter_self_average,df3_2020_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df3_2020_winter_new.iat[0,0]
unit.season = df3_2020_winter_new.iat[0,1]
unit.self_avg = df3_2020_winter_new.iat[0,2]
unit.industry_avg = df3_2020_winter_new.iat[0,3]
unit.save()
#print(df3_2020_winter_new) 

#----------------------------------南部地區年份2019(春夏秋冬)-------------------------------#
#(2019春)
df3_2019 = df3[df3['year'] == 2019]#將df3資料表格中的年份篩選為2022
df3_2019_spring = df3_2019[(df3_2019['month'] == 3) | (df3_2019['month'] == 4) | (df3_2019['month'] == 5)]
df3_2019_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2019_spring_self_avg','M_2019_spring_indusrty_avg']) #新增欄位
df3_2019_spring_self_average = sum(df3_2019_spring['self']) / 3 #算出自家用電平均
df3_2019_spring_industry_average = sum(df3_2019_spring['industry'])/3
df3_2019_spring_new.loc[3] = ['South','Spring', df3_2019_spring_self_average,df3_2019_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df3_2019_spring_new.iat[0,0]
unit.season = df3_2019_spring_new.iat[0,1]
unit.self_avg = df3_2019_spring_new.iat[0,2]
unit.industry_avg = df3_2019_spring_new.iat[0,3]
unit.save()
#print(df3_2019_spring_new) 
#(2019夏)
df3_2019_summer = df3_2019[(df3_2019['month'] == 6) | (df3_2019['month'] == 7) | (df3_2019['month'] == 8)] 
df3_2019_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2019_summer_self_avg','M_2019_summer_indusrty_avg']) #新增欄位
df3_2019_summer_self_average = sum(df3_2019_summer['self']) / 3 #算出自家用電平均
df3_2019_summer_industry_average = sum(df3_2019_summer['industry'])/3
df3_2019_summer_new.loc[3] = ['South','Summer', df3_2019_summer_self_average,df3_2019_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df3_2019_summer_new.iat[0,0]
unit.season = df3_2019_summer_new.iat[0,1]
unit.self_avg = df3_2019_summer_new.iat[0,2]
unit.industry_avg = df3_2019_summer_new.iat[0,3]
unit.save()
#print(df3_2019_summer_new) 
#(2019秋)
df3_2019_autumn = df3_2019[(df3_2019['month'] == 9) | (df3_2019['month'] == 10) | (df3_2019['month'] == 11)] 
df3_2019_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2019_autumn_self_avg','M_2019_autumn_indusrty_avg']) #新增欄位
df3_2019_autumn_self_average = sum(df3_2019_autumn['self']) / 3 #算出自家用電平均
df3_2019_autumn_industry_average = sum(df3_2019_autumn['industry'])/3
df3_2019_autumn_new.loc[3] = ['South','Autumn', df3_2019_autumn_self_average,df3_2019_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df3_2019_autumn_new.iat[0,0]
unit.season = df3_2019_autumn_new.iat[0,1]
unit.self_avg = df3_2019_autumn_new.iat[0,2]
unit.industry_avg = df3_2019_autumn_new.iat[0,3]
unit.save()
#print(df3_2019_autumn_new) 
#(2019冬)
df3_2019_winter = df3_2019[(df3_2019['month'] == 12) | (df3_2019['month'] == 1) | (df3_2019['month'] == 2)]
df3_2019_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2019_winter_self_avg','M_2019_winter_indusrty_avg']) #新增欄位
df3_2019_winter_self_average = sum(df3_2019_winter['self']) / 3 #算出自家用電平均
df3_2019_winter_industry_average = sum(df3_2019_winter['industry'])/3
df3_2019_winter_new.loc[3] = ['South','Winter', df3_2019_winter_self_average,df3_2019_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df3_2019_winter_new.iat[0,0]
unit.season = df3_2019_winter_new.iat[0,1]
unit.self_avg = df3_2019_winter_new.iat[0,2]
unit.industry_avg = df3_2019_winter_new.iat[0,3]
unit.save()
#print(df3_2019_winter_new) 



#東部地區
df4 = df_filter.copy()
df4 = df_filter.loc[(df_filter['country'] == '台東縣') | (df_filter['country'] == '花蓮縣') ]
#----------------------------------東部地區年份2023(春夏秋冬)-------------------------------#
#(2023春)
df4_2023 = df4[df4['year'] == 2023]#將df4資料表格中的年份篩選為2023
df4_2023_spring = df4_2023[(df4_2023['month'] == 3) | (df4_2023['month'] == 4) | (df4_2023['month'] == 5)]
df4_2023_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2023_spring_self_avg','M_2023_spring_indusrty_avg']) #新增欄位
df4_2023_spring_self_average = sum(df4_2023_spring['self']) / 3 #算出自家用電平均
df4_2023_spring_industry_average = sum(df4_2023_spring['industry'])/3
df4_2023_spring_new.loc[3] = ['East','Spring', df4_2023_spring_self_average,df4_2023_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df4_2023_spring_new.iat[0,0]
unit.season = df4_2023_spring_new.iat[0,1]
unit.self_avg = df4_2023_spring_new.iat[0,2]
unit.industry_avg = df4_2023_spring_new.iat[0,3]
unit.save()

#(2023夏)
df4_2023_summer = df4_2023[(df4_2023['month'] == 6) | (df4_2023['month'] == 7) | (df4_2023['month'] == 8)]
df4_2023_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2023_summer_self_avg','M_2023_summer_indusrty_avg']) #新增欄位
df4_2023_summer_self_average = sum(df4_2023_summer['self']) / 3 #算出自家用電平均
df4_2023_summer_industry_average = sum(df4_2023_summer['industry'])/3
df4_2023_summer_new.loc[3] = ['East','Summer', df4_2023_summer_self_average,df4_2023_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df4_2023_summer_new.iat[0,0]
unit.season = df4_2023_summer_new.iat[0,1]
unit.self_avg = df4_2023_summer_new.iat[0,2]
unit.industry_avg = df4_2023_summer_new.iat[0,3]
unit.save()

#(2023秋)
df4_2023_autumn = df4_2023[(df4_2023['month'] == 9) | (df4_2023['month'] == 10) | (df4_2023['month'] == 11)]
df4_2023_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2023_autumn_self_avg','M_2023_autumn_indusrty_avg']) #新增欄位
df4_2023_autumn_self_average = sum(df4_2023_autumn['self']) / 3 #算出自家用電平均
df4_2023_autumn_industry_average = sum(df4_2023_autumn['industry'])/3
df4_2023_autumn_new.loc[3] = ['East','Autumn', df4_2023_autumn_self_average,df4_2023_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df4_2023_autumn_new.iat[0,0]
unit.season = df4_2023_autumn_new.iat[0,1]
unit.self_avg = df4_2023_autumn_new.iat[0,2]
unit.industry_avg = df4_2023_autumn_new.iat[0,3]
unit.save()

#(2023冬)
df4_2023_winter = df4_2023[(df4_2023['month'] == 12) | (df4_2023['month'] == 1) | (df4_2023['month'] == 2)] 
df4_2023_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2023_winter_self_avg','M_2023_winter_indusrty_avg']) #新增欄位
df4_2023_winter_self_average = sum(df4_2023_winter['self']) / 3 #算出自家用電平均
df4_2023_winter_industry_average = sum(df4_2023_winter['industry'])/3
df4_2023_winter_new.loc[3] = ['East','Winter', df4_2023_winter_self_average,df4_2023_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2023
unit.area = df4_2023_winter_new.iat[0,0]
unit.season = df4_2023_winter_new.iat[0,1]
unit.self_avg = df4_2023_winter_new.iat[0,2]
unit.industry_avg = df4_2023_winter_new.iat[0,3]
unit.save()

#----------------------------------東部地區年份2022(春夏秋冬)-------------------------------#
#(2022春)
df4_2022 = df4[df4['year'] == 2022]#將df4資料表格中的年份篩選為2022
df4_2022_spring = df4_2022[(df4_2022['month'] == 3) | (df4_2022['month'] == 4) | (df4_2022['month'] == 5)]
df4_2022_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2022_spring_self_avg','M_2022_spring_indusrty_avg']) #新增欄位
df4_2022_spring_self_average = sum(df4_2022_spring['self']) / 3 #算出自家用電平均
df4_2022_spring_industry_average = sum(df4_2022_spring['industry'])/3
df4_2022_spring_new.loc[3] = ['East','Spring', df4_2022_spring_self_average,df4_2022_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df4_2022_spring_new.iat[0,0]
unit.season = df4_2022_spring_new.iat[0,1]
unit.self_avg = df4_2022_spring_new.iat[0,2]
unit.industry_avg = df4_2022_spring_new.iat[0,3]
unit.save()
#print(df4_2022_spring_new) 
#(2022夏)
df4_2022_summer = df4_2022[(df4_2022['month'] == 6) | (df4_2022['month'] == 7) | (df4_2022['month'] == 8)]
df4_2022_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2022_summer_self_avg','M_2022_summer_indusrty_avg']) #新增欄位
df4_2022_summer_self_average = sum(df4_2022_summer['self']) / 3 #算出自家用電平均
df4_2022_summer_industry_average = sum(df4_2022_summer['industry'])/3
df4_2022_summer_new.loc[3] = ['East','Summer', df4_2022_summer_self_average,df4_2022_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df4_2022_summer_new.iat[0,0]
unit.season = df4_2022_summer_new.iat[0,1]
unit.self_avg = df4_2022_summer_new.iat[0,2]
unit.industry_avg = df4_2022_summer_new.iat[0,3]
unit.save()
#print(df4_2022_summer_new)  
#(2022秋)
df4_2022_autumn = df4_2022[(df4_2022['month'] == 9) | (df4_2022['month'] == 10) | (df4_2022['month'] == 11)]
df4_2022_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2022_autumn_self_avg','M_2022_autumn_indusrty_avg']) #新增欄位
df4_2022_autumn_self_average = sum(df4_2022_autumn['self']) / 3 #算出自家用電平均
df4_2022_autumn_industry_average = sum(df4_2022_autumn['industry'])/3
df4_2022_autumn_new.loc[3] = ['East','Autumn', df4_2022_autumn_self_average,df4_2022_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df4_2022_autumn_new.iat[0,0]
unit.season = df4_2022_autumn_new.iat[0,1]
unit.self_avg = df4_2022_autumn_new.iat[0,2]
unit.industry_avg = df4_2022_autumn_new.iat[0,3]
unit.save()
#print(df4_2022_autumn_new)  
#(2022冬)
df4_2022_winter = df4_2022[(df4_2022['month'] == 12) | (df4_2022['month'] == 1) | (df4_2022['month'] == 2)] 
df4_2022_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2022_winter_self_avg','M_2022_winter_indusrty_avg']) #新增欄位
df4_2022_winter_self_average = sum(df4_2022_winter['self']) / 3 #算出自家用電平均
df4_2022_winter_industry_average = sum(df4_2022_winter['industry'])/3
df4_2022_winter_new.loc[3] = ['East','Winter', df4_2022_winter_self_average,df4_2022_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2022
unit.area = df4_2022_winter_new.iat[0,0]
unit.season = df4_2022_winter_new.iat[0,1]
unit.self_avg = df4_2022_winter_new.iat[0,2]
unit.industry_avg = df4_2022_winter_new.iat[0,3]
unit.save()
#print(df4_2022_winter_new)  
#----------------------------------東部地區年份2021(春夏秋冬)-------------------------------#
#(2021春)
df4_2021 = df4[df4['year'] == 2021]#將df4資料表格中的年份篩選為2022
df4_2021_spring = df4_2021[(df4_2021['month'] == 3) | (df4_2021['month'] == 4) | (df4_2021['month'] == 5)]
df4_2021_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2021_spring_self_avg','M_2021_spring_indusrty_avg']) #新增欄位
df4_2021_spring_self_average = sum(df4_2021_spring['self']) / 3 #算出自家用電平均
df4_2021_spring_industry_average = sum(df4_2021_spring['industry'])/3
df4_2021_spring_new.loc[3] = ['East','Spring', df4_2021_spring_self_average,df4_2021_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df4_2021_spring_new.iat[0,0]
unit.season = df4_2021_spring_new.iat[0,1]
unit.self_avg = df4_2021_spring_new.iat[0,2]
unit.industry_avg = df4_2021_spring_new.iat[0,3]
unit.save()
#print(df4_2021_spring_new) 
#(2021夏)
df4_2021_summer = df4_2021[(df4_2021['month'] == 6) | (df4_2021['month'] == 7) | (df4_2021['month'] == 8)]
df4_2021_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2021_summer_self_avg','M_2021_summer_indusrty_avg']) #新增欄位
df4_2021_summer_self_average = sum(df4_2021_summer['self']) / 3 #算出自家用電平均
df4_2021_summer_industry_average = sum(df4_2021_summer['industry'])/3
df4_2021_summer_new.loc[3] = ['East','Summer', df4_2021_summer_self_average,df4_2021_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df4_2021_summer_new.iat[0,0]
unit.season = df4_2021_summer_new.iat[0,1]
unit.self_avg = df4_2021_summer_new.iat[0,2]
unit.industry_avg = df4_2021_summer_new.iat[0,3]
unit.save()
#print(df4_2021_summer_new)
#(2021秋)
df4_2021_autumn = df4_2021[(df4_2021['month'] == 9) | (df4_2021['month'] == 10) | (df4_2021['month'] == 11)] 
df4_2021_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2021_autumn_self_avg','M_2021_autumn_indusrty_avg']) #新增欄位
df4_2021_autumn_self_average = sum(df4_2021_autumn['self']) / 3 #算出自家用電平均
df4_2021_autumn_industry_average = sum(df4_2021_autumn['industry'])/3
df4_2021_autumn_new.loc[3] = ['East','Autumn', df4_2021_autumn_self_average,df4_2021_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df4_2021_autumn_new.iat[0,0]
unit.season = df4_2021_autumn_new.iat[0,1]
unit.self_avg = df4_2021_autumn_new.iat[0,2]
unit.industry_avg = df4_2021_autumn_new.iat[0,3]
unit.save()
#print(df4_2021_autumn_new)
#(2021冬)
df4_2021_winter = df4_2021[(df4_2021['month'] == 12) | (df4_2021['month'] == 1) | (df4_2021['month'] == 2)] 
df4_2021_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2021_winter_self_avg','M_2021_winter_indusrty_avg']) #新增欄位
df4_2021_winter_self_average = sum(df4_2021_winter['self']) / 3 #算出自家用電平均
df4_2021_winter_industry_average = sum(df4_2021_winter['industry'])/3
df4_2021_winter_new.loc[3] = ['East','Winter', df4_2021_winter_self_average,df4_2021_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2021
unit.area = df4_2021_winter_new.iat[0,0]
unit.season = df4_2021_winter_new.iat[0,1]
unit.self_avg = df4_2021_winter_new.iat[0,2]
unit.industry_avg = df4_2021_winter_new.iat[0,3]
unit.save()
#print(df4_2021_winter_new)
#----------------------------------東部地區年份2020(春夏秋冬)-------------------------------#
#(2020春)
df4_2020 = df4[df4['year'] == 2020]#將df4資料表格中的年份篩選為2022
df4_2020_spring = df4_2020[(df4_2020['month'] == 3) | (df4_2020['month'] == 4) | (df4_2020['month'] == 5)]
df4_2020_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2020_spring_self_avg','M_2020_spring_indusrty_avg']) #新增欄位
df4_2020_spring_self_average = sum(df4_2020_spring['self']) / 3 #算出自家用電平均
df4_2020_spring_industry_average = sum(df4_2020_spring['industry'])/3
df4_2020_spring_new.loc[3] = ['East','Spring', df4_2020_spring_self_average,df4_2020_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df4_2020_spring_new.iat[0,0]
unit.season = df4_2020_spring_new.iat[0,1]
unit.self_avg = df4_2020_spring_new.iat[0,2]
unit.industry_avg = df4_2020_spring_new.iat[0,3]
unit.save()
#print(df4_2020_spring_new)  
#(2020夏)
df4_2020_summer = df4_2020[(df4_2020['month'] == 6) | (df4_2020['month'] == 7) | (df4_2020['month'] == 8)]
df4_2020_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2020_summer_self_avg','M_2020_summer_indusrty_avg']) #新增欄位
df4_2020_summer_self_average = sum(df4_2020_summer['self']) / 3 #算出自家用電平均
df4_2020_summer_industry_average = sum(df4_2020_summer['industry'])/3
df4_2020_summer_new.loc[3] = ['East','Summer', df4_2020_summer_self_average,df4_2020_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df4_2020_summer_new.iat[0,0]
unit.season = df4_2020_summer_new.iat[0,1]
unit.self_avg = df4_2020_summer_new.iat[0,2]
unit.industry_avg = df4_2020_summer_new.iat[0,3]
unit.save()
#print(df4_2020_summer_new)  
#(2020秋)
df4_2020_autumn = df4_2020[(df4_2020['month'] == 9) | (df4_2020['month'] == 10) | (df4_2020['month'] == 11)]
df4_2020_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2020_autumn_self_avg','M_2020_autumn_indusrty_avg']) #新增欄位
df4_2020_autumn_self_average = sum(df4_2020_autumn['self']) / 3 #算出自家用電平均
df4_2020_autumn_industry_average = sum(df4_2020_autumn['industry'])/3
df4_2020_autumn_new.loc[3] = ['East','Autumn', df4_2020_autumn_self_average,df4_2020_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df4_2020_autumn_new.iat[0,0]
unit.season = df4_2020_autumn_new.iat[0,1]
unit.self_avg = df4_2020_autumn_new.iat[0,2]
unit.industry_avg = df4_2020_autumn_new.iat[0,3]
unit.save()
#print(df4_2020_autumn_new) 
#(2020冬)
df4_2020_winter = df4_2020[(df4_2020['month'] == 12) | (df4_2020['month'] == 1) | (df4_2020['month'] == 2)]
df4_2020_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2020_winter_self_avg','M_2020_winter_indusrty_avg']) #新增欄位
df4_2020_winter_self_average = sum(df4_2020_winter['self']) / 3 #算出自家用電平均
df4_2020_winter_industry_average = sum(df4_2020_winter['industry'])/3
df4_2020_winter_new.loc[3] = ['East','Winter', df4_2020_winter_self_average,df4_2020_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2020
unit.area = df4_2020_winter_new.iat[0,0]
unit.season = df4_2020_winter_new.iat[0,1]
unit.self_avg = df4_2020_winter_new.iat[0,2]
unit.industry_avg = df4_2020_winter_new.iat[0,3]
unit.save()
#print(df4_2020_winter_new)  

#----------------------------------東部地區年份2019(春夏秋冬)-------------------------------#
#(2019春)
df4_2019 = df4[df4['year'] == 2019]#將df4資料表格中的年份篩選為2022
df4_2019_spring = df4_2019[(df4_2019['month'] == 3) | (df4_2019['month'] == 4) | (df4_2019['month'] == 5)]
df4_2019_spring_new = pd.DataFrame(columns=['area', 'season', 'M_2019_spring_self_avg','M_2019_spring_indusrty_avg']) #新增欄位
df4_2019_spring_self_average = sum(df4_2019_spring['self']) / 3 #算出自家用電平均
df4_2019_spring_industry_average = sum(df4_2019_spring['industry'])/3
df4_2019_spring_new.loc[3] = ['East','Spring', df4_2019_spring_self_average,df4_2019_spring_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df4_2019_spring_new.iat[0,0]
unit.season = df4_2019_spring_new.iat[0,1]
unit.self_avg = df4_2019_spring_new.iat[0,2]
unit.industry_avg = df4_2019_spring_new.iat[0,3]
unit.save()
#print(df4_2019_spring_new)  
#(2019夏)
df4_2019_summer = df4_2019[(df4_2019['month'] == 6) | (df4_2019['month'] == 7) | (df4_2019['month'] == 8)]
df4_2019_summer_new = pd.DataFrame(columns=['area', 'season', 'M_2019_summer_self_avg','M_2019_summer_indusrty_avg']) #新增欄位
df4_2019_summer_self_average = sum(df4_2019_summer['self']) / 3 #算出自家用電平均
df4_2019_summer_industry_average = sum(df4_2019_summer['industry'])/3
df4_2019_summer_new.loc[3] = ['East','Summer', df4_2019_summer_self_average,df4_2019_summer_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df4_2019_summer_new.iat[0,0]
unit.season = df4_2019_summer_new.iat[0,1]
unit.self_avg = df4_2019_summer_new.iat[0,2]
unit.industry_avg = df4_2019_summer_new.iat[0,3]
unit.save()
#print(df4_2019_summer_new) 
#(2019秋)
df4_2019_autumn = df4_2019[(df4_2019['month'] == 9) | (df4_2019['month'] == 10) | (df4_2019['month'] == 11)] 
df4_2019_autumn_new = pd.DataFrame(columns=['area', 'season', 'M_2019_autumn_self_avg','M_2019_autumn_indusrty_avg']) #新增欄位
df4_2019_autumn_self_average = sum(df4_2019_autumn['self']) / 3 #算出自家用電平均
df4_2019_autumn_industry_average = sum(df4_2019_autumn['industry'])/3
df4_2019_autumn_new.loc[3] = ['East','Autumn', df4_2019_autumn_self_average,df4_2019_autumn_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df4_2019_autumn_new.iat[0,0]
unit.season = df4_2019_autumn_new.iat[0,1]
unit.self_avg = df4_2019_autumn_new.iat[0,2]
unit.industry_avg = df4_2019_autumn_new.iat[0,3]
unit.save()
#print(df4_2019_autumn_new) 
#(2019冬)
df4_2019_winter = df4_2019[(df4_2019['month'] == 12) | (df4_2019['month'] == 1) | (df4_2019['month'] == 2)]
df4_2019_winter_new = pd.DataFrame(columns=['area', 'season', 'M_2019_winter_self_avg','M_2019_winter_indusrty_avg']) #新增欄位
df4_2019_winter_self_average = sum(df4_2019_winter['self']) / 3 #算出自家用電平均
df4_2019_winter_industry_average = sum(df4_2019_winter['industry'])/3
df4_2019_winter_new.loc[3] = ['East','Winter', df4_2019_winter_self_average,df4_2019_winter_industry_average]
pd.set_option('display.float_format', '{:.2f}'.format) #取消科學符號 並取小數點第二位
unit = models.alldata()
unit.year = 2019
unit.area = df4_2019_winter_new.iat[0,0]
unit.season = df4_2019_winter_new.iat[0,1]
unit.self_avg = df4_2019_winter_new.iat[0,2]
unit.industry_avg = df4_2019_winter_new.iat[0,3]
unit.save()
#print(df4_2019_winter_new) 



