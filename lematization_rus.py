from __future__ import division
import nltk
import collections
import numpy as np
from common_functions import get_words, total_sentences, prepare_dataset
from pymongo import MongoClient
import pymorphy2
import time
import string


def extract_words(text):
    words = []
    morph = pymorphy2.MorphAnalyzer()
    punct = set(string.punctuation)
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if word not in punct and word != "-":
                p = morph.parse(word)[0]
                if word != p.normal_form:
                    words.append(word)

    word = collections.namedtuple('word', ['words', 'unique_words'])
    return word(len(words), len(np.unique(words)))


def extract_features(data):

    extr_words = extract_words(data)

    words = extr_words.words
    unique_words = extr_words.unique_words

    total_w = len(get_words(data))
    total_unique_w = len(np.unique(get_words(data)))
    total_s = total_sentences(data)

    feature1 = words/total_w*100
    feature2 = unique_words/total_w*100
    feature3 = unique_words/total_unique_w
    feature4 = words/total_s
    feature5 = unique_words/total_s

    # return [feature1, feature2, feature3, feature4, feature5]
    print feature1
    return [feature1]


def get_test_data():

    grades = ['1', '3', '6', '9']

    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/rus/word/"
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['lem-rus']
    features_collection.drop()

    for text in dataset:
        text_features = {"grade": text.grade,
                         "features": extract_features(text.data)}
        features_collection.insert_one(text_features)

start = time.time()
get_test_data()
print str(time.time() - start) + " sec"
