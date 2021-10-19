import pandas as pd
import tomotopy as tp
import os
from konlpy.tag import Kkma
import re


def create_noun():

    kkma = Kkma()
    path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\2020년2월~2020년2월"
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)

    remove_list = ['기자', '네이버', '채널', '구독', '주세', '아이뉴스', '영상', '영상보기', '보기', '가기', '무단', '무단전재', '전재', '배포', '금지',
                   '아이', '24', '뉴스', '24', '서상', '서상혁', '머니', '머니투데이', '투데이', '전혜영', '편집', '편집자주', '자주', '아시아', '아시아경제',
                   '파이낸셜', '파이낸셜뉴스', '요즘', '등장', '현장',  '부문',  '때문',  '활용',  '한편',  '수익',  '중인',  '도입',  '메인',  '년생',  '당기',
                   ]


    f = open("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\명사 추출\\ex1.txt", 'w')
    for i in file_list:
        csv = pd.read_csv("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\2020년2월~2020년2월\\%s" % i)
        print(i, len(csv['text_content']))
        for i, line in enumerate(csv['text_content']):
            nouns = kkma.nouns(line)
            for j in nouns:
                j = re.sub('[\d+]', '', j)
                for k in remove_list:
                    j = re.sub(k, '', j)
                if len(j) >= 2:
                    data = j + ", "
                    f.write(data)
            if i % 10 == 0:
                print('Document #{} has been loaded'.format(i))

    f.close()

#create_noun()

def topic():
    file = open('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\명사 추출\\ex1.txt', 'r')
    lines = file.readlines()
    file.close()
    nouns = lines[0].split(',')
    print(len(nouns), nouns[0])
    remove_list = []
    # for i in remove_list:
    #     nouns = re.sub(nouns, '', i)


    # stop_list = ['연합뉴스']
    # for i in stop_list:
    #     print(i)
    #
    # nouns.remove('연합뉴스')

    model = tp.LDAModel(k=30, alpha=0.1, eta=0.01, min_cf=5)
    #LDAModel을 생성합니다.
    # 토픽의 개수(k)는 20개, alpha 파라미터는 0.1, eta 파라미터는 0.01
    # 전체 말뭉치에 5회 미만 등장한 단어들은 제거할 겁니다.

    model.add_doc(nouns)

    # model의 num_words나 num_vocabs 등은 train을 시작해야 확정됩니다.
    # 따라서 이 값을 확인하기 위해서 train(0)을 하여 실제 train은 하지 않고
    # 학습 준비만 시킵니다.
    # num_words, num_vocabs에 관심 없다면 이부분은 생략해도 됩니다.
    model.train(0)
    print('Total words:', model.num_words)
    print('Vocab size:', model.num_vocabs)

    # 다음 구문은 train을 총 200회 반복하면서,
    # 매 단계별로 로그 가능도 값을 출력해줍니다.
    # 혹은 단순히 model.train(200)으로 200회 반복도 가능합니다.
    for i in range(200):
        print('Iteration {}\tLL per word: {}'.format(i, model.ll_per_word))
        model.train(1)

    # 학습된 토픽들을 출력해보도록 합시다.
    for i in range(model.k):
        # 토픽 개수가 총 20개이니, 0~19번까지의 토픽별 상위 단어 10개를 뽑아봅시다.
        res = model.get_topic_words(i, top_n=10)
        print('Topic #{}'.format(i), end='\t')
        print(', '.join(w for w, p in res))

topic()