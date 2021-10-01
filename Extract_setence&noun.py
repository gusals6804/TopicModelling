from konlpy.tag import Kkma, Okt
from pandas import DataFrame as df
import pandas as pd
import time
import re
import os

kkma = Kkma()

nouns_list = []

special_symbol = re.compile('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"＜ⓒ＞\d+]')
pattern_symbol = re.compile('뉴스')
remove_list = ['기자', '네이버', '채널', '구독', '주세', '아이뉴스', '영상', '영상보기', '보기', '가기', '무단', '무단전재', '전재', '배포', '금지', '아이', '24', '뉴스', '24', '서상', '서상혁'
               '머니', '머니투데이', '투데이', '전혜영', '편집', '편집자주', '자주', '아시아', '아시아경제', '파이낸셜', '파이낸셜뉴스', '요즘', '등장']

def extract_nouns(dir_name):
    path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\%s" % (dir_name)
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)

    sum = 0
    noun_sum = []
    try:
        for file in file_list:
            csv = pd.read_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\%s\\%s" % (dir_name, file))
            for i, line in enumerate(csv['text_content']):
                sentences = kkma.sentences(line)
                print(sentences)
                clean_nouns = []
                for sentence in sentences:
                    nouns = kkma.nouns(sentence)
                    for noun in nouns:
                        noun = re.sub(special_symbol, '', noun)
                        for remove in remove_list:
                            noun = re.sub(remove, '', noun)
                        if len(noun) > 1:
                            clean_nouns.append(noun)
                nouns_list.append(clean_nouns)
                noun_sum += clean_nouns
                print(nouns_list[i])
                sum += 1
                if i % 10 == 0:
                    print('Document #{} has been loaded'.format(i))
    except:
        pass


    directory = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\기사 단어\\"
    data = df(data={'sentences': nouns_list})
    data.to_pickle(os.path.join(directory, '%s.pkl' % dir_name))
    #data.to_csv(os.path.join(directory, '%s_process_nouns.csv' % ('2020년2월~2020년2월')), encoding='utf-8-sig')
    print(sum)
    #print(noun_sum)
    print(len(set(noun_sum)))

year = [2013]
for i in year:
    for j in range(11, 13):
        dir_name = '%d년%d월~%d년%d월' % (i, j, i, j)
        print(dir_name)
        extract_nouns(dir_name)
