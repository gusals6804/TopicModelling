from konlpy.tag import Kkma, Okt
from pandas import DataFrame as df
from gensim.models.word2vec import Word2Vec
import pandas as pd
import logging
import time
import re
import os
import matplotlib as mpl
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

start = time.time()
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

kkma = Kkma()
mc = Okt()


def word2vec():
    word_list = []
    path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 2013~2015 pkl"
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)
    for i in file_list:
        df = pd.read_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 2013~2015 pkl\\%s" % i)
        for j in df['sentences']:
            if len(j) > 1:
                #print(j)
                word_list.append(j)

    print(len(word_list))
    #print(word_list)
    embedding_model = Word2Vec(word_list, size=200, window=10, min_count=5, iter=500, sg=1, sample=1e-3, hs=0)


    # embedding_model2 = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\stock_summary_model_01.model')
    # embedding_model2.wv.save_word2vec_format("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\word_vector_sample.bin", binary=True)

    # model2 = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\2013~2015_report_size20_win10_min5_iter500_hs0_intersect_ko2')
    # model2.wv.save_word2vec_format("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\ko\\2013~2015_report_size20_win10_min5_iter500_hs0_intersect_ko2.bin", binary=True)
    #
    # prev_model = 'C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\ko\\2013~2015_report_size20_win10_min5_iter500_hs0_intersect_ko2.bin'
    # embedding_model.intersect_word2vec_format(fname=prev_model, lockf=1.0, binary=True)
    model_name = "2013~2015_report_size200_win10_min5_iter500_hs0"
    embedding_model.save('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\%s' % model_name)
    word_vector = embedding_model.wv


def tsne_plot(model):
    labels = []
    tokens = []

    mpl.rcParams['axes.unicode_minus'] = False
    plt.rc('font', family='NanumGothic')

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    print(labels)
    print(len(labels))
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values[:300]:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()



def cluster(model, file, model_name):


    result = model.wv  # 어휘의 feature vector
    topic = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\토픽 모델링 결과\\%s' % file)
    #print(result.vocab.keys())
    #vocabs = result.vocab.keys()
    vocabs = []
    for i in topic['sentences']:
        for j in i:
            vocabs.append(j)

    print(len(vocabs))
    # clean_file = open('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\클러스터전처리.txt', 'r')
    # lines = clean_file.readlines()
    # clean_file.close()
    # remove_list = lines[0].split(', ')

    remove_list = []
    word_vectors = []
    clean_vocabs = []

    for i in vocabs:
        for remove in remove_list:
            i = re.sub(remove, '', i)
        if len(i) > 1:
            clean_vocabs.append(i)

    for v in clean_vocabs:
        try:
            word_vectors.append(result[v])
        except:
            print(v)
            clean_vocabs.remove(v)

    num_clusters = 50  # int(len(clean_vocabs) / 5)  # int(word_vectors.shape[0]/50) # 어휘 크기의 1/5나 평균 5단어
    print(num_clusters)
    num_clusters = int(num_clusters)

    kmeans_clustering = KMeans(n_clusters=num_clusters)
    idx = kmeans_clustering.fit_predict(word_vectors)
    #idx = DBSCAN(eps=1000, min_samples=2).fit(word_vectors)
    print(id)
    idx = list(idx)
    print(len(vocabs))
    print(len(idx))
    names = clean_vocabs
    print(names)
    word_centroid_map = {names[i]: idx[i] for i in range(len(idx))}

    dfIndustry = pd.DataFrame(columns=["cluster", "keyword"])
    for c in range(num_clusters):
        # 클러스터 번호를 출력
        print("\ncluster {}".format(c))

        words = []
        cluster_values = list(word_centroid_map.values())
        for i in range(len(cluster_values)):
            if (cluster_values[i] == c):
                words.append(list(word_centroid_map.keys())[i])

        if len(words) == 1:
            print(words)

        rowIndustry = [c, words]
        dfIndustry.loc[len(dfIndustry)] = rowIndustry

    print(dfIndustry)

    clean_file = open('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\클러스터전처리.txt', 'r')
    lines = clean_file.readlines()
    clean_file.close()
    remove_list = lines[0].split(', ')

    count = 0
    for i in dfIndustry['keyword']:
        clean_v = []
        for j in i:
            print(j)
            for remove in remove_list:
                j = re.sub(remove, '', j)
            if len(j) > 1:
                clean_v.append(j)

        dfIndustry['keyword'][count] = clean_v
        count += 1

    print(dfIndustry)


    print("time: ", time.time() - start)
    dfIndustry.to_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\클러스터링최종\\군집_%s.pkl" % (model_name))

word2vec()
#tsne_plot(model)


# path_dir = "C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\토픽 모델링 결과"
# file_list = os.listdir(path_dir)
# file_list.sort()
# print(file_list)
#
# for file in file_list:
#     cluster(model, file)

# model_name = '2013~2015_report_size20_win20_min5_iter1000_hs0'
# model = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\%s' % model_name)
# file = '3년.pkl'
#
# cluster(model, file, model_name)
#sim(['기계', '펄프'], model)