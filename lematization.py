from __future__ import division
import nltk
import collections
import numpy as np
from common_functions import get_words, total_sentences, prepare_dataset
from pymongo import MongoClient
from nltk.stem.wordnet import WordNetLemmatizer


from nltk.corpus import wordnet as wn
import time

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return None


def extract_words(text):
    words = []
    lmtzr = WordNetLemmatizer()
    for sent in nltk.sent_tokenize(text):

        for chunk in nltk.pos_tag(nltk.word_tokenize(sent)):
            if isinstance(chunk, tuple):
                if penn_to_wn(chunk[1]) is not None:
                    if chunk[0] != lmtzr.lemmatize(chunk[0], penn_to_wn(chunk[1])):
                        words.append(chunk[0])

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

    # grades = ['K-1', '4-5', '9-10']
    grades = ['2-3', '6-8', '11-CCR']
    # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']

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
