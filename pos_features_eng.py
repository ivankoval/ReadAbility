from __future__ import division
import nltk
import collections
import numpy as np
from common_functions import get_words, total_sentences, prepare_dataset
from pymongo import MongoClient


nouns = ['NN', 'NNP', 'NNPS', 'NNS']
verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adjectives = ['JJ', 'JJR', 'JJS']
adverbs = ['RB', 'RBR', 'RBS', 'WRB']
prepositions = ['IN', 'TO']

content = ['NN', 'NNP', 'NNPS', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'CD', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'WRB']
functional = ['CC', 'DT', 'EX', 'FW', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$']


def extract_words(text, pos_type):
    words = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.pos_tag(nltk.word_tokenize(sent)):
            if isinstance(chunk, tuple):
                if chunk[1] in pos_type:
                    words.append(chunk[0])
    word = collections.namedtuple('word', ['words', 'unique_words'])
    return word(len(words), len(np.unique(words)))


def extract_features(data, pos):

    extr_words = extract_words(data, pos)

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

    return [feature1, feature2, feature3, feature4, feature5]


def get_test_data():
    pos_set = [nouns]

    # grades = ['K-1', '4-5', '9-10']
    grades = ['2-3', '6-8', '11-CCR']
    # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']

    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/"
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['pos-eng']
    features_collection.drop()

    for text in dataset:
        features = []
        for pos in pos_set:
            features += extract_features(text.data, pos)

        text_features = {"grade": text.grade, "features": features}
        features_collection.insert_one(text_features)


get_test_data()