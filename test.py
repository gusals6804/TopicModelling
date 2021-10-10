from gensim.models.word2vec import Word2Vec
# #
# # model2 = Word2Vec.load('C:/Users/82105/Desktop/한글Word2Vec범용/ko.bin')
# # model2.wv.save_word2vec_format("word_vector_sample.bin",binary=True)
# # sentences = [
# #     ['오늘도', '온다'],
# #     ['나는', '고프다']
# #              ]
# # model2 = Word2Vec(sentences, size=10, window=3, min_count=1, workers=1, iter=1)
# # file_name2 = 'word_vector_sample.bin'
# #
# # model2.intersect_word2vec_format(fname=file_name2, binary=True)

import pickle
# import pandas as pd
# data = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\기사 단어\\2013년1월~2013년1월.pkl')
# print(data)
#
# count = 0
# for i in data['sentences']:
#     for j in i:
#         count += 1
#
# print(count)

#model2 = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\ko\\ko.bin')
#model2.wv.save_word2vec_format("C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\ko\\ko2.bin", binary=True)
# sentences = [
#     ['오늘도', '온다'],
#     ['나는', '고프다']
#              ]
# model2 = Word2Vec(sentences, size=10, window=3, min_count=1, workers=1, iter=1)
# file_name2 = 'word_vector_sample.bin'
#
# model2.intersect_word2vec_format(fname=file_name2, binary=True

# model32 = Word2Vec.load('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\word2vec_model\\ko\\ko2.bin')

import pandas as pd
data = pd.read_pickle('C:\\Users\\gusals\\Desktop\\현민\\딥러닝 특론\\리포트 6개월 토픽 결과\\201307~201312.pkl')
print(data)