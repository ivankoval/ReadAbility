# -*- coding: utf-8 -*-
from __future__ import division
import nltk
import pymorphy2
from common_functions import prepare_dataset
from pymongo import MongoClient
import time

def extract_features(data):

    morph = pymorphy2.MorphAnalyzer()

    nomn, gent, datv, accs, ablt, loct, total = 0, 0, 0, 0, 0, 0, 0

    for sent in nltk.sent_tokenize(data):
        for word in nltk.word_tokenize(sent):
            p = morph.parse(word)
            if len(p) == 1:
                for var in p:
                    if var.tag.POS == 'NOUN':
                        case = var.tag.case
                        if case == 'nomn':
                            nomn += 1
                        if case == 'gent':
                            gent += 1
                        if case == 'datv':
                            datv += 1
                        if case == 'accs':
                            accs += 1
                        if case == 'ablt':
                            ablt += 1
                        if case == 'loct':
                            loct += 1
                        if str(case) != 'None':
                            total += 1
    if total == 0:
        print "0 0 0 0 0 0"
        return [0, 0, 0, 0, 0, 0]

    print str(nomn/total*100) + " " + str(gent/total*100) + " " + str(datv/total*100) +\
          " " + str(accs/total*100) + " " + str(ablt/total*100) + " " + str(loct/total*100)
    return [nomn/total*100, gent/total*100, datv/total*100, accs/total*100, ablt/total*100, loct/total*100]


def get_test_data():

    # grades = ['test']
    grades = ['1', '3', '6', '9']

    # path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_test/rus/word/"
    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/rus/word/"

    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['case']
    features_collection.drop()

    for text in dataset:
        text_features = {"grade": text.grade, "features": extract_features(text.data)}
        features_collection.insert_one(text_features)


start = time.time()
get_test_data()
print str(time.time() - start) + " sec"
