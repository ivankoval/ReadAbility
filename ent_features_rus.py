# -*- coding: utf-8 -*-
from __future__ import division
import xml.etree.ElementTree as ElementTree
from common_functions import get_words, total_sentences, prepare_dataset
from pymongo import MongoClient
import time

def extract_entities_api(data):
    root = ElementTree.fromstring(data)
    count = 0
    for value in root.iter('value'):
        count += 1
    return count


def extract_features(data):
    root = ElementTree.fromstring(data)
    pure_text = root[0].text

    ne = extract_entities_api(data)
    tw = len(get_words(pure_text))
    ts = total_sentences(pure_text)

    feature1 = ne/tw*100
    feature2 = ne/ts*100

    return [feature1, feature2]


def get_test_data():

    grades = ['1', '3', '6', '9']
    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/ApiData/rus/ent/"
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['ent-rus']
    features_collection.drop()

    for text in dataset:
        features = extract_features(text.data.encode('utf-8'))
        text_features = {"grade": text.grade, "features": features}
        print str(features)
        features_collection.insert_one(text_features)


start = time.time()
get_test_data()
print str(time.time() - start) + " sec"
