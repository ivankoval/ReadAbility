
from __future__ import division
import os
import math
import nltk
from nltk import ngrams


def calc_pp(text, n):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if len(token) > 1]
    # tokens = [token.lower() for token in tokens]
    text_length = len(tokens)
    n_tokens = list(ngrams(tokens, n))
    sum_prob = 0
    for item in sorted(set(n_tokens)):
        if n_tokens.count(item) != 1:
            prob = n_tokens.count(item)/len(n_tokens)
            sum_prob += math.log(prob, 2)
            # sum_prob += n_tokens.count(item) * math.log(prob, 2) - math.log(math.factorial(n_tokens.count(item)), 2)

    entropy = -(1/text_length)*sum_prob
    pp = math.pow(2, entropy)
    return pp


def extract_features(path):
    with open(path, "r") as myfile:
        data = myfile.read().replace('\n', ' ')
        data = data.decode('utf-8')
    features = []
    for i in xrange(1, 6):
        features.append(calc_pp(data, i))
    return features


def get_test_data():
    # grades = ['K-1', '4-5', '9-10']
    # grades = ['2-3', '6-8', '11-CCR']
    # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
    # path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/"
    grades = ['1', '3', '4', '6', '8', '10', '11', '17']
    path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/Russian/textsbygrade/"

    features_file = open('features_lm_rus.txt', 'w+')

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