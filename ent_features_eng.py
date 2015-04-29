# TODO 1: total number of entity mentions per document
# TODO 2: total number of unique entity mentions per document
# TODO 3: average number of entity mentions per sentence
# TODO 4: average number of unique entity mentions per sentence


from __future__ import division
import nltk
import string
import collections
import os
import numpy as np


def total_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return len(words)


def total_sentences(text):
    sent = nltk.sent_tokenize(text)
    return len(sent)


def extract_entities(text):
    named_entities = []
    # proper_nouns = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.chunk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)), binary=True):
            if isinstance(chunk, nltk.tree.Tree):
                if chunk.label() == 'NE':
                    for entity in chunk.leaves():
                        named_entities.append(entity[0])
            # if isinstance(chunk, tuple):
            #     if chunk[1] == 'NNP':
            #         proper_nouns.append(chunk[0])
    entities = collections.namedtuple('Entities', ['ne', 'unique_ne'])
    return entities(len(named_entities), len(np.unique(named_entities)))


def extract_features(path):
    with open(path, "r") as myfile:
        data = myfile.read().replace('\n', '')
        data = data.decode('utf-8')

    extr_entities = extract_entities(data)
    ne = extr_entities.ne
    tw = total_words(data)
    ts = total_sentences(data)
    feature1 = ne/tw*100
    feature2 = ne/ts*100

    return [feature1, feature2]


def get_test_data():
    # grades = ['K-1', '4-5', '9-10']
    # grades = ['2-3', '6-8', '11-CCR']
    grades = ['1', '2', '3']
    # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
    path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/temp/"
    features_file = open('features.txt', 'w+')

    for grade in grades:
        path_to_grade = path + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':
                features = extract_features(path_to_grade + filename)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

    features_file.close()


get_test_data()