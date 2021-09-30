from pandas import DataFrame as df
import re
import pandas as pd
from gensim.models.word2vec import Word2Vec
from sklearn import decomposition
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from spherecluster import SphericalKMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

def cluster(model, file, model_name):

    result = model.wv  # 어휘의 feature vector
    topic = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\topic\\%s.pkl' % file)
    #print(result.vocab.keys())
    #vocabs = result.vocab.keys()
    vocabs = []
    for i in topic['sentences']:
        for j in i:
            vocabs.append(j)

    print(len(vocabs))

    clean_file = open('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\data\\클러스터전처리.txt', 'r')
    lines = clean_file.readlines()
    clean_file.close()
    remove_list = lines[0].split(', ')

    word_vectors = []
    clean_vocabs = []

    clean = ['코로']
    for v in vocabs:
        if v in clean:
            v = re.sub('코로', '코로나', v)
            print(v)
        try:
            word_vectors.append(result[v])
            clean_vocabs.append(v)
        except:
            print(v)
            clean_vocabs.remove(v)

    num_clusters = 40 #int(len(word_vectors) / 10)  # int(word_vectors.shape[0]/50) # 어휘 크기의 1/5나 평균 5단어
    print(word_vectors[0])
    num_clusters = int(num_clusters)

    # tsne = TSNE(n_components=2)
    # reduced_X = tsne.fit_transform(word_vectors)
    # idx = DBSCAN(eps=4, min_samples=20).fit(word_vectors)
    #
    pca = decomposition.PCA(n_components=10).fit(word_vectors)
    reduced_X = pca.transform(word_vectors)

    # elbow(word_vectors)
    kmeans_clustering = KMeans(init="k-means++", n_clusters=num_clusters, random_state=0)
    idx = kmeans_clustering.fit_predict(reduced_X)

    # skm = SphericalKMeans(n_clusters=40)
    # idx = skm.fit_predict(word_vectors)
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

    count = 0
    last_word = []
    for i in dfIndustry['keyword']:
        clean_v = []
        for j in i:
            if j not in remove_list:
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

    dfIndustry.to_pickle("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\군집\\군집_%s_pca10_KMeans.pkl" % model_name)


def elbow(x):
    sse = []
    for i in range(1, 50):
        km = KMeans(n_clusters=i, init='k-means++', random_state=0)
        km.fit(x)
        sse.append(km.inertia_)

    plt.plot(range(1, 50), sse, marker='o')
    plt.savefig('./cluster.png')


model_name = '2017_report_size20_win10_min10_iter500_hs0'
model = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\최종정리\\word2vec\\%s' % model_name)
file = '2017'
#cluster(model, file, model_name)