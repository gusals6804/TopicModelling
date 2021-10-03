import os

from time import sleep
import re
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame as df


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

def crawler(date):
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&sid2=259&sid1=101&mid=shm&sort=0&date=" + str(date)

    # 데이터 프레임을 생성할 리스트 기사 제목, 기사 내용
    text_headline_list = []
    text_list = []
    time_list = []

    # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
    # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨 (Redirect)
    totalpage = find_news_totalpage(url + "&page=10000")
    print(totalpage)

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
            cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', cleaned_text)
            cleaned_text_headline = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', cleaned_text_headline)
            cleaned_text_time = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', cleaned_text_time)


            text_list.append(cleaned_text)
            text_headline_list.append(cleaned_text_headline)
            time_list.append(cleaned_text_time)

    data = df(data={'text_headline': text_headline_list, 'text_content': text_list, 'text_time': time_list})
    data.to_csv('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\%s_news.csv' % date, encoding='ms949')
    print(data)

#20200328 날짜 형식
crawler(20200328)