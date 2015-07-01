# -*- coding: utf-8 -*-
from __future__ import division
from common_functions import get_words, total_sentences, prepare_dataset
from pymongo import MongoClient
import time

const = r"bcdfghjklmnpqrstvwxyz"
vow = r'aeiou'


def count_syllables(s):
    vowels = [u'а', u'е', u'и', u'у', u'о', u'я', u'ё', u'э', u'ю', u'я', u'ы']
    syl_count = 0
    for ch in s:
        if ch in vowels:
            syl_count += 1
    return syl_count


# average number of syllables per word
def feature_one(text):
    words = get_words(text)
    syllables_sum = 0
    for word in words:
        syllables_sum += count_syllables(word)
    return syllables_sum/len(words)


# percentage of poly-syll. words per doc.
def feature_two(text):
    words = get_words(text)
    poly_syllables_words = 0
    for word in words:
        if count_syllables(word) > 1:
            poly_syllables_words += 1
    return poly_syllables_words/len(words)*100


# average number of poly-syll. words per sent.
def feature_three(text):
    words = get_words(text)
    poly_syllables_words = 0
    for word in words:
        if count_syllables(word) > 1:
            poly_syllables_words += 1
    return poly_syllables_words/total_sentences(text)


# average number of characters per word
def feature_four(text):
    words = get_words(text)
    characters_sum = 0
    for word in words:
        characters_sum += len(word)
    return characters_sum/len(words)


# Chall-Dale difficult words rate per doc.
def feature_five(text):
    path_difficult_words = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/DaleChallEasyWordList.txt"
    words = get_words(text)
    difficult_words_sum = 0

    with open(path_difficult_words, 'r') as f:
        difficult_words = f.readlines()

    for word in words:
        if word not in difficult_words:
            difficult_words_sum += 1
    return 0.0496 * len(words)/total_sentences(text) + 0.1579 * difficult_words_sum/len(words) * 100 + 3.6365


# average number of words per sentence
def feature_six(text):
    return len(get_words(text))/total_sentences(text)


# Flesch-Kincaid score
def feature_seven(text):
    words = get_words(text)
    syllables_sum = 0
    for word in words:
        syllables_sum += count_syllables(word)

    return 0.39 * len(words)/total_sentences(text) + 11.8 * syllables_sum/len(words) - 15.59


# total number of words per document
def feature_eight(text):
    return len(get_words(text))


def extract_features(data):

    return [feature_one(data), feature_two(data), feature_three(data), feature_four(data),
            feature_six(data), feature_seven(data), feature_eight(data)]
    # return [feature_eight(data)]


def get_test_data():
    grades = ['1', '3', '6', '9']
    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/rus/word/"

    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['shallow-rus']
    features_collection.drop()

    for text in dataset:
        features = extract_features(text.data)
        text_features = {"grade": text.grade, "features": features}
        print text.grade
        features_collection.insert_one(text_features)


start = time.time()
get_test_data()
print str(time.time() - start) + " sec"