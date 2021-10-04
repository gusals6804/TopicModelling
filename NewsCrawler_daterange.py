import os
from time import sleep
import re
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame as df
import calendar

def find_news_totalpage(url):
    # 당일 기사 목록 전체를 알아냄
    try:
        totlapage_url = url
        request_content = requests.get(totlapage_url)
        document_content = BeautifulSoup(request_content.content, 'html.parser')
        headline_tag = document_content.find('div', {'class': 'paging'}).find('strong')
        regex = re.compile(r'<strong>(?P<num>\d+)')
        match = regex.findall(str(headline_tag))
        return int(match[0])
    except Exception:
        return 0


def make_news_date(start_year, start_month, end_year, end_month):

    # 지정한 날짜 범위 이름으로 디렉토리 생성
    directory_name = str(start_year) + "년" + str(start_month) +"월" + "~" + str(end_year) + "년" + str(end_month) + "월"
    directory = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\%s" % directory_name
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print('Error: creating directory.' + directory)

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

                #yyyymmdd 형태로 맞춰서 리스트에 추가
                date.append((str(year) + str(month) + str(month_day)))

    date
    return date, directory


def crawler(date, directory):

    for one_day in date:
        url = "https://news.naver.com/main/list.nhn?mode=LS2D&sid2=259&sid1=101&mid=shm&sort=0&date=" + str(one_day)

        # 데이터 프레임을 생성할 리스트 기사 제목, 기사 내용, 기사 작성 시간
        text_headline_list = []
        text_list = []
        time_list = []

        # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
        # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨 (Redirect)
        totalpage = find_news_totalpage(url + "&page=10000")
        print("요일: " + str(one_day), ", totalpage: " + str(totalpage))

        for page in range(1, totalpage + 1):
            url = url + "&page=" + str(page)
            print(page)
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')

            # 각 페이지에 있는 기사들 가져오기
            post_temp = soup.select('.list_body newsflash_body .type06_headline li dl')
            post_temp.extend(soup.select('.newsflash_body .type06 li dl'))

            # 각 페이지에 있는 기사들의 url 저장
            post = []
            for line in post_temp:
                post.append(line.a.get('href'))  # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
            del post_temp
            # print(post)

            for line in post:
                sleep(0.01)

                news_html = requests.get(line).text

                try:
                    news_soup = BeautifulSoup(news_html, 'html.parser')
                except:
                    continue

                try:
                    tag_headline = news_soup.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                    text_headline = ''
                    text_headline = text_headline + str(tag_headline[0].find_all(text=True))
                    if not text_headline:  # 공백일 경우 기사 제외 처리
                        continue

                    tag_text = news_soup.find_all('div', {'id': 'articleBodyContents'})
                    text_content = ''
                    text_content = text_content + str(tag_text[0].find_all(text=True))
                    if not text_content:  # 공백일 경우 기사 제외 처리
                        continue

                    tag_time = news_soup.find_all('span', {'class': 't11'})
                    text_time = ''
                    text_time = text_time + str(tag_time[0].find_all(text=True))
                    if not text_time:  # 공백일 경우 기사 제외 처리
                        continue

                except:
                    continue

                remove_text = ['본문 내용', '플레이어', '오류를 우회하기 위한 함수 추가']
                for i in remove_text:
                    text_content = re.sub(i, '', text_content)
                cleaned_text = re.sub('[a-zA-Z]', '', text_content)
                cleaned_text_headline = re.sub('[a-zA-Z]', '', text_headline)
                cleaned_text_time = re.sub('[a-zA-Z]', '', text_time)
                cleaned_text = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', cleaned_text)
                cleaned_text_headline = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', cleaned_text_headline)
                cleaned_text_time = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', cleaned_text_time)


                text_list.append(cleaned_text)
                text_headline_list.append(cleaned_text_headline)
                time_list.append(cleaned_text_time)

        data = df(data={'text_headline': text_headline_list, 'text_content': text_list, 'text_time': time_list})
        data.to_pickle(os.path.join(directory, '%s.pkl' % str(one_day)))
        #data.to_csv(os.path.join(directory, '%s_news.csv' % str(one_day)), encoding='utf-8-sig')
        print(data)
        print(str(one_day) + "뉴스 크롤링 csv 저장 완료")

# 시작연도, 시작 월, 끝나는 연도, 끝나는 월
year = [2020]

for i in year:
    for j in range(3, 7):
        date, directory = make_news_date(i, j, i, j)
        crawler(date, directory)