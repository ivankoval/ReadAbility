# TODO percent of adjectives (tokens) per document
# TODO percent of unique adjectives (types) per document
# TODO ratio of unique adjectives per total unique words in a document
# TODO average number of adjectives per sentence
# TODO average number of unique adjectives per sentence

from __future__ import division
import nltk
import string
import collections
import os
import numpy as np

nouns = ['NN', 'NNP', 'NNPS', 'NNS']
verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adjectives = ['JJ', 'JJR', 'JJS']
adverbs = ['RB', 'RBR', 'RBS', 'WRB']
prepositions = ['IN', 'TO']

content = ['NN', 'NNP', 'NNPS', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'CD', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'WRB']
functional = ['CC', 'DT', 'EX', 'FW', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$']


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


def extract_words(text, pos_type):
    words = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.pos_tag(nltk.word_tokenize(sent)):
            if isinstance(chunk, tuple):
                if chunk[1] in pos_type:
                    words.append(chunk[0])
    word = collections.namedtuple('word', ['words', 'unique_words'])
    return word(len(words), len(np.unique(words)))


def extract_features(path, pos_type):
    with open(path, "r") as myfile:
        data = myfile.read().replace('\n', '')
        data = data.decode('utf-8')

    extr_words = extract_words(data, pos_type)

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
    # grades = ['K-1', '4-5', '9-10']
    grades = ['2-3', '6-8', '11-CCR']
    # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
    path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/"

    path_to_features = "/Users/Ivan/PycharmProject/ReadAbility/features/pos_features_eng.txt"
    features_file = open(path_to_features, 'w+')

    for grade in grades:
        path_to_grade = path + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':

                features = extract_features(path_to_grade + filename, nouns)
                for feature in features:
                    features_file.write(str(feature) + '\n')

                features = extract_features(path_to_grade + filename, verbs)
                for feature in features:
                    features_file.write(str(feature) + '\n')

                features = extract_features(path_to_grade + filename, adjectives)
                for feature in features:
                    features_file.write(str(feature) + '\n')

                features = extract_features(path_to_grade + filename, adverbs)
                for feature in features:
                    features_file.write(str(feature) + '\n')

                features = extract_features(path_to_grade + filename, prepositions)
                for feature in features:
                    features_file.write(str(feature) + '\n')

                features = extract_features(path_to_grade + filename, content)
                for feature in features:
                    features_file.write(str(feature) + '\n')

                features = extract_features(path_to_grade + filename, functional)
                for feature in features:
                    features_file.write(str(feature) + '\n')

                features_file.write(str(grade) + '\n')

    features_file.close()


get_test_data()