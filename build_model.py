# -*- coding: utf-8 -*-
import nltk
import time
from nltk.probability import SimpleGoodTuringProbDist, FreqDist
from nltk import ngrams
from common_functions import prepare_dataset
from pymongo import MongoClient


def create_lm(path_to_data, grades, f_type):
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')

    for grade in grades:
        print grade + " grade"
        start_total = time.time()
        client.drop_database(f_type + '_' + grade)
        db = client[f_type + '_' + grade]

        for n in xrange(1, 3):
            print str(n) + " gram"
            start = time.time()
            fd_dict = dict()
            # TODO separate dataset on grades

            for text in dataset:
                if text.grade == grade:
                    fd_dict[text.name] = FreqDist()
            fd_dict['all'] = FreqDist()

            for text in dataset:
                if text.grade == grade:

                    tokens = nltk.word_tokenize(text.data)
                    tokens_l = [token.lower() for token in tokens]

                    for key in fd_dict:
                        if key != text.name:
                            n_grams = ngrams(tokens_l, n)
                            fd_dict[key].update(n_grams)

            for key in fd_dict:
                lm_collection = db[key]
                fd = fd_dict[key]
                sgt = SimpleGoodTuringProbDist(fd)
                prob_many = list()

                for fd_key in fd:
                    prob_many.append({"type": fd_key, "n-gram": n, "count": fd[fd_key], "prob": sgt.prob(fd_key)})

                if prob_many:
                    lm_collection.insert_many(prob_many)

            print str(time.time() - start) + " sec"

        print str(time.time() - start_total) + " sec total"

def display():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['lm-rus-word-pos_3']
    lm_collection = db['all']
    # db = client['features']
    # lm_collection = db['lm-eng']
    for n_gram in lm_collection.find():
        print n_gram


def run(lang, type_):
    path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_test/"

    if lang == 'eng':
        grades = ['2-3', '6-8', '11-CCR']
    if lang == 'rus':
        grades = ['1', '3', '6', '9']

    create_lm(path + lang + '/' + type_ + '/', grades, 'lm-' + lang + '-' + type_)


# display()
run('eng', 'word-pos')
