# -*- coding: utf-8 -*-
from __future__ import division
from sklearn import svm
from pymongo import MongoClient
from common_functions import get_words, total_sentences, prepare_dataset


class TestData:
    data = []
    target = []

    def __init__(self):
        self.data = []
        self.target = []


def load_data(path):
    with open('/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/' + path, 'r') as myfile:
        data = myfile.readlines()
    return data

def make_features():
    test_data = TestData()

    words = load_data('words.txt')
    prefixes = load_data('pref.txt')
    suffixes = load_data('suff.txt')

    dict_1 = dict()
    dict_2 = dict()
    i = 0
    for prefix in prefixes:
        prefix = prefix.replace('\r\n', '')
        dict_1[prefix] = i
        i += 1
    i = 0
    for suffix in suffixes:
        suffix = suffix.replace('\r\n', '')
        dict_2[suffix] = i
        i += 1

    for word in words:
        word = word.replace('\r\n', '')
        type_ = word[word.index(',')+1:]
        word = word[:word.index(',')]

        prefix_cand = []
        suffix_cand = []
        for prefix in prefixes:
            prefix = prefix.replace('\r\n', '')
            try:
                if word.index(prefix) == 0:
                    prefix_cand.append(prefix)
            except:
                pass

        if len(prefix_cand) == 0:
            prefix = 'none'
        else:
            prefix = max(prefix_cand, key=len)

        for suffix in suffixes:
            suffix = suffix.replace('\r\n', '')
            try:
                if word.index(suffix) > 2:
                    suffix_cand.append(suffix)
            except:
                pass

        if len(suffix_cand) == 0:
            suffix = 'none'
        else:
            suffix = max(suffix_cand, key=len)

        arr = []
        for key in dict_1:
            if key != prefix:
                arr.append(0)
            else:
                arr.append(1)

        for key in dict_2:
            if key != suffix:
                arr.append(0)
            else:
                arr.append(1)

        test_data.data.append(arr)
        test_data.target.append(type_)

    clf_svm = svm.SVC(kernel='linear', C=1)
    clf_svm.fit(test_data.data, test_data.target)

    return clf_svm

def extract_features(data, clf):
    prefixes = load_data('pref.txt')
    suffixes = load_data('suff.txt')

    dict_1 = dict()
    dict_2 = dict()
    i = 0
    for prefix in prefixes:
        prefix = prefix.replace('\r\n', '')
        dict_1[prefix] = i
        i += 1
    i = 0
    for suffix in suffixes:
        suffix = suffix.replace('\r\n', '')
        dict_2[suffix] = i
        i += 1

    words = get_words(data)
    borrowed_num = 0
    original_num = 0

    for word in words:
        word = word.lower()
        word = word.encode('utf-8')

        prefix_cand = []
        suffix_cand = []
        for prefix in prefixes:
            prefix = prefix.replace('\r\n', '')
            try:
                if word.index(prefix) == 0:
                    prefix_cand.append(prefix)
            except:
                pass

        if len(prefix_cand) == 0:
            prefix = 'none'
        else:
            prefix = max(prefix_cand, key=len)

        for suffix in suffixes:
            suffix = suffix.replace('\r\n', '')
            try:
                if word.index(suffix) > 2:
                    suffix_cand.append(suffix)
            except:
                pass

        if len(suffix_cand) == 0:
            suffix = 'none'
        else:
            suffix = max(suffix_cand, key=len)

        arr = []
        for key in dict_1:
            if key != prefix:
                arr.append(0)
            else:
                arr.append(1)

        for key in dict_2:
            if key != suffix:
                arr.append(0)
            else:
                arr.append(1)

        if suffix != 'none' or prefix != 'none':
            if clf.predict(arr)[0] == 'borrowed':
                borrowed_num += 1
            if clf.predict(arr)[0] == 'original':
                original_num += 1
    return [borrowed_num/len(words)*100, original_num/len(words)*100]

def get_test_data():

    clf = make_features()

    grades = ['1', '3', '6', '9']
    # path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_test/rus/word/"
    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/rus/word/"
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['inclusions']
    features_collection.drop()

    for text in dataset:
        features = extract_features(text.data, clf)
        text_features = {"grade": text.grade, "features": features}
        print text.grade + " " + text.name + " " + str(features)
        features_collection.insert_one(text_features)


get_test_data()
