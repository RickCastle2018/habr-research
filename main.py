# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime
import gensim.downloader
import xgboost as xgb
from sklearn.model_selection import train_test_split
import re
import matplotlib.pyplot as plt

print(list(gensim.downloader.info()['models'].keys()))

glove_vectors = gensim.downloader.load('word2vec-ruscorpora-300')

words=list(glove_vectors.vocab.keys())

cutsymbs=[":", "_"]
cleanwords=[]
for word in words:
    clean = word[0]
    i=0
    while word[i+1] not in cutsymbs:
        clean+=word[i+1]
        i+=1
    cleanwords.append(clean)

glove_vectors.most_similar('apple_NOUN')

cleanwords

words

glove_vectors.get_vector('яблоко_NOUN')

glove_vectors.get_vector(words[0]).shape

fail300=np.ones(300)
fail300

def FindWordInVocab(word):
    word=word.lower()
    if word in cleanwords:
        index=cleanwords.index(word)
        return glove_vectors.get_vector(words[index])
    else:
        return fail300

FindWordInVocab("пень")

data=pd.read_json("data.json")

data

wordlist = data["teaser"][0].split()
#list all the word in feature dataset (teasers)

def EncodeData(wordlist=wordlist):
    vector_words = []
    for word in wordlist:
        vector_words.append(FindWordInVocab(word))
    return vector_words
#Из списка слов делает вектор

ans=np.array(EncodeData())
print(ans.shape)

len(wordlist)

#datetime.datetime(*ti.strptime("2007-03-04T21:08:12", "%Y-%m-%dT%H:%M:%S")[:6])

todrop=["pubdate", "text"]

for i in todrop:
    data2=data.drop(i, axis=1)

data2=data2.drop("pubdate", axis=1)

features = np.array(data2.drop("rating", axis=1))

features=data2["teaser"]
#features - это только текст тизеров

labels=np.array(data2["rating"])

features

labels

"""Нужно из тизеров сделать числа, а потом передавать это как массив 1000 x 300, где 300 длина эмбеддинга"""

reg = re.compile('[^а-яА-Я ^a-zA-Z]')
testcleanstr=reg.sub('', features[0])
testcleanstr

X=[]
reg = re.compile('[^а-яА-Я ^a-zA-Z]')
for str in features:
    X.append(reg.sub('', str))
X

X1=EncodeData(X[0])
X1
#Привести все слова в нач. форму, а дальше закодировать

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

X_train.shape

model=xgb.XGBClassifier()

# from sklearn.linear

model.fit(X_train, y_train)



predictions=model.predict(X_test)


plt.plot(predictions[:100], label="predticted views")
plt.plot(y_test[:100], label="true views")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=2, mode="expand", borderaxespad=0.)
plt.ylim(0, 50000)
#plt.ylegend()
plt.xlabel("Article Number")
plt.ylabel("Views")

plt.plot(y_test)
