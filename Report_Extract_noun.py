from konlpy.tag import Kkma, Okt
from pandas import DataFrame as df
import pandas as pd
import time
import re
import os
import openpyxl
import calendar
import numpy as np

kkma = Kkma()

def make_report_date(start_year, start_month, end_year, end_month):
    # 지정한 날짜 범위 이름으로 디렉토리 생성
    # directory_name = str(start_year) + "년" + str(start_month) + "월" + "~" + str(end_year) + "년" + str(end_month) + "월"
    # directory = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\%s" % directory_name
    # try:
    #     if not os.path.exists(directory):
    #         os.mkdir(directory)
    # except OSError:
    #     print('Error: creating directory.' + directory)

    # 지정한 범위 안의 날짜를 구해서 리스트에 저장
    date = []
    for year in range(start_year, end_year + 1):
        if start_year == end_year:
            year_startmonth = start_month
            year_endmonth = end_month
        else:
            if year == start_year:
                year_startmonth = start_month
                year_endmonth = 12
            elif year == end_year:
                year_startmonth = 1
                year_endmonth = end_month
            else:
                year_startmonth = 1
                year_endmonth = 12

        for month in range(year_startmonth, year_endmonth + 1):
            for month_day in range(1, calendar.monthrange(year, month)[1] + 1):
                if len(str(month)) == 1:
                    month = "0" + str(month)
                if len(str(month_day)) == 1:
                    month_day = "0" + str(month_day)

                # yyyymmdd 형태로 맞춰서 리스트에 추가
                date_str = str(year) + "-" + str(month) + "-" + str(month_day)
                date.append(date_str)
    print(date)
    return date


special_symbol = re.compile('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"＜ⓒ＞\d+]')
# remove_list = ['기자', '네이버', '채널', '구독', '주세', '아이뉴스', '영상', '영상보기', '보기', '가기', '무단', '무단전재', '전재', '배포', '금지', '아이',
#                '24', '뉴스', '24', '서상', '서상혁', '머니', '머니투데이', '투데이', '전혜영', '편집', '편집자주', '자주', '아시아', '아시아경제', '파이낸셜',
#                '파이낸셜뉴스', '요즘', '등장']


def extract_nouns(start_year, start_month, end_year, end_month):
    start = time.time()

    path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\산업 리포트\\리포트"
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)

    nouns_list = []
    sum = 0
    noun_sum = []
    text = []

    clean_file = open('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\리포트 전처리.txt', 'r')
    lines = clean_file.readlines()
    clean_file.close()
    remove_list = lines[0].split(', ')
    print(len(set(remove_list)), remove_list)

    for file in file_list:
        xls = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\산업 리포트\\리포트\\%s" % file
        print(file)
        wb = openpyxl.load_workbook(xls)
        sheet_name = wb.get_sheet_names()
        print(sheet_name)

        date_list = []
        summary = []
        for sheet in sheet_name:
            sheet = wb[sheet]

            value = pd.DataFrame(sheet.values)
            value2 = value.iloc[12:, :11]
            date_list += list(value2.iloc[1:, 0])
            summary += list(value2.iloc[1:, 10])

        print(summary)
        print(date_list)
        data = df(data={'Date': date_list, 'Summary': summary})
        data['date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d', errors='coerce')
        print(data['date'])
        #print(data['Summary'])


        date = make_report_date(start_year, start_month, end_year, end_month)
        for i in date:

            range_date = data.loc[data['date'] == i]
            #print(range_date)
            for j in range_date['Summary']:
                text.append(j)

        for i, line in enumerate(text):

            nouns = kkma.nouns(line)

            print(nouns)
            clean_nouns = []
            for noun in nouns:
                noun = re.sub(special_symbol, '', noun)
                if noun not in remove_list and len(noun) > 1:
                # for remove in remove_list:
                #     noun = re.sub(remove, '', noun)
                # if len(noun) > 1:
                    clean_nouns.append(noun)
            nouns_list.append(clean_nouns)
            #noun_sum += clean_nouns
            print(nouns_list[i])
            sum += 1
            if i % 10 == 0:
                print('Document #{} has been loaded'.format(i))

        #print(len(noun_sum))

    directory = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 2016~2020 pkl\\"
    noun_data = df(data={'sentences': nouns_list})
    noun_data.to_pickle(os.path.join(directory, '%s_%s~%s_%s.pkl' % (start_year, start_month, end_year, end_month)))
    noun_data.to_csv(os.path.join(directory, '%s_%s~%s_%s_process_report_nouns.csv' % (start_year, start_month, end_year, end_month)), encoding='utf-8-sig')
    print(sum)

    print("time :", time.time() - start)


def preprocess(noun, remove):
    clean_nouns = []
    set_noun = set(noun)
    set_remove = set(remove)
    clean = set_noun - set_remove
    for noun in clean:
        if len(noun) > 1:
            clean_nouns.append(noun)

    return clean_nouns

year = [2016]
for i in year:
    for j in range(1, 2):
        extract_nouns(i, j, i, j)

