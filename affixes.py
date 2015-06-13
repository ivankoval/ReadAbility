# -*- coding: utf-8 -*-
from __future__ import division
from common_functions import get_words, total_sentences, prepare_dataset
from pymongo import MongoClient


def load_data(path):
    with open('/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/' + path, 'r') as myfile:
        data = myfile.readlines()
    return data

def extract_features(data):
    prefixes = load_data('pref.txt')
    suffixes = load_data('suff.txt')
    prefix_num = 0
    suffix_num = 0
    words = get_words(data)

    for word in words:
        word = word.lower()
        word = (word.encode('utf-8')).lower()

        prefix_cand = []
        suffix_cand = []

        for prefix in prefixes:
            prefix = prefix.replace('\r\n', '')
            try:
                if word.index(prefix) == 0:
                    prefix_cand.append(prefix)
            except:
                pass

        if len(prefix_cand) != 0:
            prefix_num += 1

        for suffix in suffixes:
            suffix = suffix.replace('\r\n', '')
            try:
                if word.index(suffix) > 2:
                    suffix_cand.append(suffix)
            except:
                pass

        if len(suffix_cand) != 0:
            suffix_num += 1

    # print [prefix_num/len(words), suffix_num/len(words)]
    # return [prefix_num/len(words), suffix_num/len(words)]
    return [prefix_num/len(words)]



def get_test_data():

    grades = ['1', '3', '6', '9']
    # grades = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10-11']
    # path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_test/rus/word/"
    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/rus/word/"
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['affixes']
    features_collection.drop()

    for text in dataset:
        text_features = {"grade": text.grade,
                         "features": extract_features(text.data)}
        features_collection.insert_one(text_features)


get_test_data()

