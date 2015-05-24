from __future__ import division
import nltk
import collections
import numpy as np
from common_functions import get_words, total_sentences, prepare_dataset
from pymongo import MongoClient


def extract_entities(text):
    named_entities = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.chunk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)), binary=True):
            if isinstance(chunk, nltk.tree.Tree):
                if chunk.label() == 'NE':
                    for entity in chunk.leaves():
                        named_entities.append(entity[0])
    entities = collections.namedtuple('Entities', ['ne', 'unique_ne'])
    return entities(len(named_entities), len(np.unique(named_entities)))


def extract_features(data):
    extr_entities = extract_entities(data)

    ne = extr_entities.ne
    tw = len(get_words(data))
    ts = total_sentences(data)

    feature1 = ne/tw*100
    feature2 = ne/ts*100

    return [feature1, feature2]


def get_test_data():
    # grades = ['K-1', '4-5', '9-10']
    grades = ['2-3', '6-8', '11-CCR']
    # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/"

    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['ent-eng']
    features_collection.drop()

    for text in dataset:
        text_features = {"grade": text.grade,
                         "features": extract_features(text.data)}
        features_collection.insert_one(text_features)


get_test_data()
