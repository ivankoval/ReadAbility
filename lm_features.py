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

    pipe = [{'$group': {'_id': '$n-gram', 'total': {'$sum': '$count'}}}, {'$match': {'_id': n}}]
    docs = lm.aggregate(pipeline=pipe)
    for doc in docs:
        zero_prob = lm.find({"n-gram": n, "count": 1}).count()/doc['total']

    for item in set(n_grams):

        found_lm = lm.find_one({"type": item, "n-gram": n})

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


def extract_features(data, grades):
    features = []
    for grade in grades:
        print grade

        client = MongoClient('mongodb://localhost:27017/')
        db = client.language_models_eng
        lm_collection = db[grade]

        start = time.time()
        for i in xrange(1, 4):
            print i
            features.append(calc_pp(data, lm_collection, i))
        print str(time.time() - start) + " sec"
    return features


def get_test_data():

    # grades = ['K-1', '4-5', '9-10']
    grades = ['2-3', '6-8', '11-CCR']
    # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
    path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/"

    # grades = ['1', '3', '6', '9']
    # path_to_data = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/Russian/dictant/"

    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['lm-eng']
    features_collection.drop()

    for text in dataset:
        print text.name
        text_features = {"grade": text.grade,
                         "features": extract_features(text.data,  grades)}
        features_collection.insert_one(text_features)


get_test_data()
