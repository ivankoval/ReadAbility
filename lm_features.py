from __future__ import division
import math
import nltk
from nltk import ngrams
from common_functions import prepare_dataset
from pymongo import MongoClient
import time


def calc_pp(text, lm, n):

    tokens = nltk.word_tokenize(text)

    tokens = [token.lower() for token in tokens]
    n_grams = list(ngrams(tokens, n))
    text_length = len(tokens)
    sum_prob = 0

    count_one = 0
    count_sum = 0

    for d in lm:
        count_sum += d['count']
        if d['count'] == 1:
            count_one += 1

    if count_one == 0:
        count_one = 1

    zero_prob = count_one/count_sum

    for item in set(n_grams):

        found_lm = None

        for d in lm:
            if tuple(d['type']) == item:
                found_lm = d
                break

        if found_lm:
            prob = found_lm["prob"]
        else:
            prob = zero_prob

        count_w = n_grams.count(item)
        sum_prob += count_w * math.log(prob, 2) - math.log(math.factorial(count_w), 2)

    entropy = -(1/text_length)*sum_prob
    pp = math.pow(2, entropy)
    print pp
    return pp


def extract_features(f_type, text, grades):
    features = []
    for grade in grades:
        print grade

        client = MongoClient('mongodb://localhost:27017/')
        db = client[f_type + '_' + grade]
        if text.grade == grade:
            lm_collection = db[text.name]
        else:
            lm_collection = db['all']

        # start = time.time()
        for i in xrange(1, 3):
            print i
            features.append(calc_pp(text.data, list(lm_collection.find({"n-gram": i})), i))
        # print str(time.time() - start) + " sec"
    return features


def get_test_data(f_type, path_to_data, grades):

    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features[f_type]
    features_collection.drop()

    start = time.time()

    for text in dataset:
        print text.name
        text_features = {"grade": text.grade,
                         "features": extract_features(f_type, text,  grades)}
        features_collection.insert_one(text_features)

    print str(time.time() - start) + " sec total"

get_test_data('lm-eng-ig', "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/ig/", ['K-1', '4-5', '9-10'])
