from gensim.models.word2vec import Word2Vec
import pandas as pd
import os
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

def word2vec(file, size, window, min, iter, hs):
    word_list = []
    path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\data\\%s" % file
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)
    for i in file_list:
        df = pd.read_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\data\\2017\\%s" % i)
        print(df)
        for j in df['sentences']:
            if len(j) > 1:
                #print(j)
                word_list.append(j)

    print(len(word_list))
    print(word_list)
    embedding_model = Word2Vec(word_list, size=size, window=window, min_count=min, iter=iter, sg=1, sample=1e-3, hs=hs, workers=8)


    # embedding_model2 = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\stock_summary_model_01.model')
    # embedding_model2.wv.save_word2vec_format("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\word_vector_sample.bin", binary=True)

    # model2 = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\2013~2015_report_size20_win10_min5_iter500_hs0_intersect_ko2')
    # model2.wv.save_word2vec_format("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\ko\\2013~2015_report_size20_win10_min5_iter500_hs0_intersect_ko2.bin", binary=True)
    #
    # prev_model = 'C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\word_vector_sample.bin'
    # embedding_model.intersect_word2vec_format(fname=prev_model, lockf=1.0, binary=True)

    model_name = "%s_report_size%d_win%d_min%d_iter%d_hs%d" % (file, size, window, min, iter, hs)
    embedding_model.save('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\word2vec\\%s' % model_name)

def most_sim(word):
    path_dir = "./word2vec_test/"
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)

    for i in file_list:
        model = Word2Vec.load('./word2vec_test/%s' % i)
        df = pd.DataFrame(model.wv.most_similar(word, topn=10), columns=['단어', '유사도'])
        print(df)


def sim(word_1, word_2):
    path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\word2vec_test\\"
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)

    file_name = []
    sim_result = []
    for i in file_list:
        model = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\word2vec_test\\%s' % i)
        file_name.append(i)
        sim_result.append(model.wv.similarity(word_1, word_2))
        print(model.wv.similarity(word_1, word_2))

    df = pd.DataFrame(data={'모델': file_name, '유사도': sim_result})
    print(df)





#word2vec('2017', 20, 10, 10, 500, 0)
sim('제약', '의료')
#most_sim('2차전지')



