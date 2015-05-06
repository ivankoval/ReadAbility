# -*- coding: utf-8 -*-
from __future__ import division
import os
import string
import nltk
import re
const = r"bcdfghjklmnpqrstvwxyz"
vow = r'aeiou'


def total_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return words


def count_syllables(s):
    vowels = [u'а', u'е', u'и', u'у', u'о', u'я', u'ё', u'э', u'ю', u'я', u'ы']
    syl_count = 0
    for ch in s:
        if ch in vowels:
            syl_count += 1
    return syl_count


def total_sentences(text):
    sent = nltk.sent_tokenize(text)
    return len(sent)


# average number of syllables per word
def feature_one(text):
    words = total_words(text)
    syllables_sum = 0
    for word in words:
        syllables_sum += count_syllables(word)
    return syllables_sum/len(words)


# percentage of poly-syll. words per doc.
def feature_two(text):
    words = total_words(text)
    poly_syllables_words = 0
    for word in words:
        if count_syllables(word) > 1:
            poly_syllables_words += 1
    return poly_syllables_words/len(words)*100


# average number of poly-syll. words per sent.
def feature_three(text):
    words = total_words(text)
    poly_syllables_words = 0
    for word in words:
        if count_syllables(word) > 1:
            poly_syllables_words += 1
    return poly_syllables_words/total_sentences(text)


# average number of characters per word
def feature_four(text):
    words = total_words(text)
    characters_sum = 0
    for word in words:
        characters_sum += len(word)
    return characters_sum/len(words)


# Chall-Dale difficult words rate per doc.
def feature_five(text):
    path_difficult_words = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/DaleChallEasyWordList.txt"
    words = total_words(text)
    difficult_words_sum = 0

    with open(path_difficult_words, 'r') as f:
        difficult_words = f.readlines()

    for word in words:
        if word not in difficult_words:
            difficult_words_sum += 1
    return 0.0496 * len(words)/total_sentences(text) + 0.1579 * difficult_words_sum/len(words) * 100 + 3.6365


# average number of words per sentence
def feature_six(text):
    return len(total_words(text))/total_sentences(text)


# Flesch-Kincaid score
def feature_seven(text):
    words = total_words(text)
    syllables_sum = 0
    for word in words:
        syllables_sum += count_syllables(word)

    return 0.39 * len(words)/total_sentences(text) + 11.8 * syllables_sum/len(words) - 15.59


# total number of words per document
def feature_eight(text):
    return len(total_words(text))


def extract_features(path):
    with open(path, "r") as myfile:
        text = myfile.read().replace('\n', '')
        text = text.decode('utf-8')

    return [feature_one(text), feature_two(text), feature_three(text), feature_four(text),
            feature_five(text), feature_six(text), feature_seven(text), feature_eight(text)]


def get_test_data():
    grades = ['1', '3', '6', '9']
    path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/Russian/dictant/"
    path_to_features = "/Users/Ivan/PycharmProject/ReadAbility/features/shallow_features_rus.txt"
    features_file = open(path_to_features, 'w+')

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