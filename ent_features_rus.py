# -*- coding: utf-8 -*-
from __future__ import division
import xml.etree.ElementTree as ElementTree
import nltk
import string
import os


def total_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return len(words)


def total_sentences(text):
    sent = nltk.sent_tokenize(text)
    return len(sent)


def extract_entities_api(path):
    tree = ElementTree.parse(path)
    root = tree.getroot()
    count = 0
    for value in root.iter('value'):
        count += 1
    return count


def extract_features(path):
    tree = ElementTree.parse(path)
    root = tree.getroot()
    data = root[0].text

    ne = extract_entities_api(path)
    tw = total_words(data)
    ts = total_sentences(data)

    feature1 = ne/tw*100
    feature2 = ne/ts*100

    return [feature1, feature2]


def get_test_data():

    grades = ['1', '3', '6', '9']

    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/ApiData/ent/"
    path_to_features = "/Users/Ivan/PycharmProject/ReadAbility/features/ent_features_rus.txt"

    features_file = open(path_to_features, 'w+')

    for grade in grades:
        path_to_grade = path_to_data + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':
                features = extract_features(path_to_grade + filename)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

    features_file.close()


get_test_data()