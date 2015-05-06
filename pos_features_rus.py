# -*- coding: utf-8 -*-
from __future__ import division
import xml.etree.ElementTree as ElementTree
import nltk
import string
import os
import numpy as np
import collections

nouns = ['S']
verbs = ['V']
adjectives = ['A']
adverbs = ['ADV']
prepositions = ['PR']

content = ['S', 'V', 'NUM', 'A', 'ADV']
functional = ['PR', 'COM', 'CONJ', 'PART', 'P', 'INTJ', 'NID']


def total_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return len(words)


def total_sentences(text):
    sent = nltk.sent_tokenize(text)
    return len(sent)


def total_unique_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return len(np.unique(words))


def extract_words(path, pos_type):
    tree = ElementTree.parse(path)
    root = tree.getroot()
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


def extract_features(path, pos_type):
    tree = ElementTree.parse(path)
    root = tree.getroot()
    data = root[0].text

    extr_words = extract_words(path, pos_type)

    words = extr_words.words
    unique_words = extr_words.unique_words

    total_w = total_words(data)
    total_unique_w = total_unique_words(data)
    total_s = total_sentences(data)

    feature1 = words/total_w*100
    feature2 = unique_words/total_w*100
    feature3 = unique_words/total_unique_w
    feature4 = words/total_s
    feature5 = unique_words/total_s

    return [feature1, feature2, feature3, feature4, feature5]


def get_test_data():
    grades = ['1', '3', '6', '9']
    # grades = ['2', '4', '7', '10-11']
    # grades = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10-11']

    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/ApiData/pos/"
    path_to_features = "/Users/Ivan/PycharmProject/ReadAbility/features/pos_features_rus.txt"

    features_file = open(path_to_features, 'w+')

    for grade in grades:
        path_to_grade = path_to_data + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':

                features = extract_features(path_to_grade + filename, nouns)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

                features = extract_features(path_to_grade + filename, verbs)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

                features = extract_features(path_to_grade + filename, adjectives)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

                features = extract_features(path_to_grade + filename, adverbs)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

                features = extract_features(path_to_grade + filename, prepositions)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

                features = extract_features(path_to_grade + filename, content)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

                features = extract_features(path_to_grade + filename, functional)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

    features_file.close()


get_test_data()
