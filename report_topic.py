import pandas as pd
import tomotopy as tp
import os
from konlpy.tag import Kkma
import re
import pandas as pd
from pandas import DataFrame as df


def create_noun(file):

    # pickle_data = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\기사 단어\\%s' % file)
    # nouns = []
    # for i in pickle_data['sentences']:
    #     nouns += i
    # print(nouns)

    nouns = []

    for i in file:
        pickle_data = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 2013~2015 pkl\\%s' % i)
        for j in pickle_data['sentences']:
            nouns += j

    print(len(nouns))

    clean_file = open('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\리포트 전처리_추가.txt', 'r')
    lines = clean_file.readlines()
    clean_file.close()
    remove_list = lines[0].split(', ')
    print(len(set(remove_list)), remove_list)
    clean = []
    for i in nouns:
        for remove in remove_list:
            i = re.sub(remove, '', i)
        i = re.sub('코로나바', '코로나바이러스', i)
        i = re.sub('르스', '메르스', i)

        if len(i) >= 2:
            clean.append(i)

    print(len(clean))
    noun_data = df(data={'clean_nouns': clean})
    noun_data.to_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월씩\\201507~201512.pkl")



def topic(pkl_file):
    # pickle_data = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 2013~2015 pkl\\%s' % pkl_file)
    # nouns = []
    # for i in pickle_data['sentences']:
    #     nouns += i
    # print(nouns)

    # nouns = []
    #
    # for i in pkl_file:
    #     pickle_data = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 2013~2015 pkl\\%s' % i)
    #     for j in pickle_data['sentences']:
    #         nouns += j
    #
    # print(len(nouns))
    #
    # clean_file = open('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\크롤링결과\\리포트 전처리_추가.txt', 'r')
    # lines = clean_file.readlines()
    # clean_file.close()
    # remove_list = lines[0].split(', ')
    # print(len(set(remove_list)), remove_list)
    # clean = []
    # for i in nouns:
    #     for remove in remove_list:
    #         i = re.sub(remove, '', i)
    #     i = re.sub('코로나바', '코로나바이러스', i)
    #     i = re.sub('르스', '메르스', i)
    #
    #     if len(i) >= 2:
    #         clean.append(i)
    #
    # print(len(clean))
    # noun_data = df(data={'clean_nouns': clean})
    # noun_data.to_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\토픽 모델링 결과\\topic_noun.pkl")

    for i in pkl_file:
        df2 = pd.read_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월씩\\%s" % i)
        for j in df2['clean_nouns']:
            if len(j) > 1:
                # print(j)
                word_list.append(j)
    print(len(word_list))

    # result = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월씩\\%s' % pkl_file)
    # clean = result['clean_nouns']

    model = tp.LDAModel(k=70, alpha=0.1, eta=0.0001, min_cf=5)
    #LDAModel을 생성합니다.
    # 토픽의 개수(k)는 20개, alpha 파라미터는 0.1, eta 파라미터는 0.01
    # 전체 말뭉치에 5회 미만 등장한 단어들은 제거할 겁니다.


    model.add_doc(word_list)

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
    for i in range(1000):
        print('Iteration {}\tLL per word: {}'.format(i, model.ll_per_word))
        model.train(1)

    # 학습된 토픽들을 출력해보도록 합시다.
    result_list = []
    for i in range(model.k):
        # 토픽 개수가 총 20개이니, 0~19번까지의 토픽별 상위 단어 10개를 뽑아봅시다.
        res = model.get_topic_words(i, top_n=15)
        print('Topic #{}'.format(i), end='\t')
        print(', '.join(w for w, p in res))
        result_word = []
        for w,p in res:
            result_word.append(w)
        result_list.append(result_word)

    #directory = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 단어\\"
    noun_data = df(data={'sentences': result_list})
    noun_data.to_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월 토픽 결과\\3년_report_topic.pkl")
    result = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월 토픽 결과\\3년_report_topic.pkl')
    print(result)

#create_noun()
word_list = []
path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월씩"
file_list = os.listdir(path_dir)
file_list.sort()
print(file_list)


topic(file_list)


# file = []
# year = [2015]
# for i in year:
#     for j in range(7, 13):
#         dir_name = '%d_%d~%d_%d.pkl' % (i, j, i, j)
#         print(dir_name)
#         file.append(dir_name)
#
# create_noun(file)
