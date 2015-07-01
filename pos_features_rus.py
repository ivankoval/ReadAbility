# -*- coding: utf-8 -*-
from __future__ import division
import xml.etree.ElementTree as ElementTree
import numpy as np
import collections
from common_functions import get_words, total_sentences, prepare_dataset
from pymongo import MongoClient
import time

nouns = ['S']
verbs = ['V']
adjectives = ['A']
adverbs = ['ADV']
prepositions = ['PR']

content = ['S', 'V', 'NUM', 'A', 'ADV']
functional = ['PR', 'COM', 'CONJ', 'PART', 'P', 'INTJ', 'NID']


def extract_words(data, pos_type):
    root = ElementTree.fromstring(data)
    words = []

    for word in root.iter('I-annotation'):
        start_word = 0
        end_word = 0
        pos_tag = ''

        for child in word:
            if child.tag == 'start':
                start_word = int(child.text)
            if child.tag == 'end':
                end_word = int(child.text)
            if child.tag == 'value':
                pos_tag = child[0].text

        if pos_tag in pos_type:
            words.append(root[0].text[start_word:end_word])

    word = collections.namedtuple('word', ['words', 'unique_words'])
    return word(len(words), len(np.unique(words)))


def extract_features(data, pos_type):
    root = ElementTree.fromstring(data)
    pure_text = root[0].text

    extr_words = extract_words(data, pos_type)

    words = extr_words.words
    unique_words = extr_words.unique_words

    total_w = len(get_words(pure_text))
    total_unique_w = len(np.unique(get_words(pure_text)))
    total_s = total_sentences(pure_text)

    feature1 = words/total_w*100
    feature2 = unique_words/total_w*100
    feature3 = unique_words/total_unique_w
    feature4 = words/total_s
    feature5 = unique_words/total_s

    return [feature1, feature2, feature3, feature4, feature5]


def get_test_data():
    pos_set = [nouns, verbs, adjectives, adverbs, prepositions]

    grades = ['1', '3', '6', '9']

    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/ApiData/rus/pos/"
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['pos-rus']
    features_collection.drop()

    for text in dataset:
        features = []
        for pos in pos_set:
            features += extract_features(text.data.encode('utf-8'), pos)

        text_features = {"grade": text.grade, "features": features}
        print str(features)
        features_collection.insert_one(text_features)


start = time.time()
get_test_data()
print str(time.time() - start) + " sec"
