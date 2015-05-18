from __future__ import print_function
import nltk
from nltk.probability import SimpleGoodTuringProbDist, FreqDist
from nltk import ngrams
from common_functions import prepare_dataset
from pymongo import MongoClient


def create_lm(path_to_data, grades):
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')
    db = client.language_models_eng

    for grade in grades:

        lm_collection = db[grade]
        lm_collection.drop()

        for n in xrange(1, 6):
            fd = FreqDist()
            for text in dataset:
                print(text.name + " " + str(n))
                if text.grade == grade:
                    tokens = nltk.word_tokenize(text.data)
                    tokens_l = [token.lower() for token in tokens]
                    n_grams = ngrams(tokens_l, n)
                    fd.update(n_grams)
            sgt = SimpleGoodTuringProbDist(fd)
            for key in fd:
                n_gram = []
                for word in key:
                    n_gram.append(word)
                prob = {"type": n_gram, "n-gram": n, "count": fd[key], "prob": sgt.prob(key)}
                lm_collection.insert_one(prob)


# create_lm("/Users/Ivan/PycharmProject/ReadAbility/DataSets/", ['Test'])
# create_lm("/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/", ['2-3'])
