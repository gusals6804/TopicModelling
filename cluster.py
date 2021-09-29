from konlpy.tag import Kkma, Okt
from pandas import DataFrame as df
from gensim.models.word2vec import Word2Vec
import pandas as pd
import logging
import time
import re
import os
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import decomposition
from sklearn.decomposition import PCA
from soyclustering import SphericalKMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
def cluster(model, file, model_name):

    result = model.wv  # 어휘의 feature vector
    topic = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월 토픽 결과\\%s' % file)
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

    clean_file = open('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\클러스터전처리.txt', 'r')
    lines = clean_file.readlines()
    clean_file.close()
    remove_list = lines[0].split(', ')


    #remove_list = []
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

    # tsne = TSNE(n_components=2)
    # reduced_X = tsne.fit_transform(word_vectors)

    pca = decomposition.PCA(n_components=20).fit(word_vectors)
    reduced_X = pca.transform(word_vectors)


    #kmeans_clustering = SphericalKMeans(n_clusters=num_clusters, max_iter=10, verbose=1,init='similar_cut')
    kmeans_clustering = KMeans(n_clusters=num_clusters)
    idx = kmeans_clustering.fit_predict(reduced_X)

    # skm = SphericalKMeans(n_clusters=10)
    # idx = skm.fit_predict(word_vectors)
    #idx = DBSCAN(eps=4, min_samples=20).fit(word_vectors)
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
    last_word = []
    for i in dfIndustry['keyword']:
        clean_v = []
        for j in i:
            for remove in remove_list:
                j = re.sub(remove, '', j)
            if len(j) > 1:
                clean_v.append(j)
        last_word += clean_v
        dfIndustry['keyword'][count] = clean_v
        count += 1

    print(len(last_word))
    print(last_word)
    # tsne_plot(model, clean_vocabs)
    print(dfIndustry)

    for i in dfIndustry['keyword']:
        print(i)
    show(model, last_word)

    dfIndustry.to_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\클러스터링최종\\군집_%s_%s_kmean_pca.pkl" % (file, model_name))

def sim(word, model):
    if len(word) >= 2:
        print(model.wv.similarity(word[0], word[1]))
    else:
        df = pd.DataFrame(model.wv.most_similar('%s' % word, topn=10), columns=['단어', '유사도'])
        print(df)

def most_sim(word, model):
    df = pd.DataFrame(model.wv.most_similar('%s' % word, topn=10), columns=['단어', '유사도'])
    print(df)

def show(model, data):
    vocab = list(model.wv.vocab)
    mpl.rcParams['axes.unicode_minus'] = False
    plt.rc('font', family='NanumGothic')

    X = model[data]

    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(X)
    df = pd.DataFrame(X_tsne, index=data, columns=["x", "y"])

    fig = plt.figure()
    fig.set_size_inches(40, 20)
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df["x"], df["y"])

    for word, pos in list(df.iterrows()):
        ax.annotate(word, pos, fontsize=12)

    plt.show()

# def viz_img(y_pred):
#     n = 10
#     fig = plt.figure(1)
#     box_index = 1
#     for cluster in range(10):
#         result = np.where(y_pred == cluster)
#         for i in np.random.choice(result[0].tolist(), n, replace=False):
#             ax = fig.add_subplot(n, n, box_index)
#             plt.imshow(x_train[i].reshape(28, 28))
#             plt.gray()
#             ax.get_xaxis().set_visible(False)
#             ax.get_yaxis().set_visible(False)
#             box_index += 1
#     plt.show()

def tsne_plot(model, clean):
    labels = []
    tokens = []

    mpl.rcParams['axes.unicode_minus'] = False
    plt.rc('font', family='NanumGothic')

    for word in clean:
        tokens.append(model[word])
        labels.append(word)

    print(labels)
    print(len(labels))
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values[:len(clean)]:
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


model_name = '2013~2015_report_size200_win10_min5_iter500_hs0'
#model_name = '2013~2015_report_size20_win10_min5_iter500_hs0_intersect'
#model_name = '2013~2015_report_size200_win10_min5_iter500_hs0_intersect_ko2'
#model_name = '2013~2015_report_size200_win10_min5_iter500_hs0_intersect_ko2_all'
model = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\%s' % model_name)
#model2 = Word2Vec.load

file = '3년_report_topic.pkl'
cluster(model, file, model_name)
#most_sim('항공', model)
# '보험', '가스', '기계', '조선', '헬스'
#sim(['은행', '통신'], model)