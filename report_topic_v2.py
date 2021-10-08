import pandas as pd
import tomotopy as tp
import os
from konlpy.tag import Kkma
import re
import pandas as pd
from pandas import DataFrame as df

def topic(pkl_file):
    word_list = []
    path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\data\\%s" % pkl_file
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)

    for i in file_list:
        data = pd.read_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\data\\%s\\%s" % (pkl_file, i))
        #print(data)
        for j in data['sentences']:
            if len(j) > 1:
                # print(j)
                word_list.append(j)
    print(len(word_list))

    # result = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월씩\\%s' % pkl_file)
    # clean = result['clean_nouns']

    model = tp.LDAModel(k=100, alpha=0.1, eta=0.0001, min_cf=5)
    #LDAModel을 생성합니다.
    # 토픽의 개수(k)는 20개, alpha 파라미터는 0.1, eta 파라미터는 0.01
    # 전체 말뭉치에 5회 미만 등장한 단어들은 제거할 겁니다.

    for i in word_list:
        model.add_doc(i)

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
    for i in range(500):
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
    noun_data.to_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\topic\\%s.pkl" % pkl_file)
    result = pd.read_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\topic\\%s.pkl" % pkl_file)
    print(result)

#topic('2017')
# result = pd.read_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\topic\\2013.pkl")
# result.to_csv("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\topic\\2013.csv", encoding='utf-8-sig')
# print(result)
