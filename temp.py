import nltk
import time
from nltk.probability import SimpleGoodTuringProbDist, FreqDist
from nltk import ngrams
from common_functions import prepare_dataset
from pymongo import MongoClient


def create_lm(path_to_data, grades):
    dataset = prepare_dataset(path_to_data, grades)

    client = MongoClient('mongodb://localhost:27017/')

    for grade in grades:
        print grade + " grade"
        start_total = time.time()
        client.drop_database('lm_eng_' + grade)
        db = client['lm_eng_' + grade]

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
                print key
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
    db = client['lm_eng_test']
    print(db.collection_names())
    lm_collection = db['all']
    for n_gram in lm_collection.find():
        print (n_gram)

# display()
# create_lm("/Users/Ivan/PycharmProject/ReadAbility/DataSets/Test/", ['test'])
create_lm("/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/", ['11-CCR'])
