__author__ = 'IvanK'

from sklearn import svm
from sklearn import linear_model
from sklearn import cross_validation
import numpy as np
import time
from pymongo import MongoClient


class TestData:
    data = []
    target = []

    def __init__(self):
        self.data = []
        self.target = []


def get_test_data(features_type):

    test_data = TestData()

    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features[features_type]

    for text_feature in features_collection.find():
        print text_feature
        test_data.target.append(text_feature['grade'])
        test_data.data.append(np.array(text_feature['features'], dtype=float))
        print text_feature['features']
        # test_data.data.append(text_feature['features'])

    return test_data


def classification(alg):
    start = time.time()

    cv = 10
    test_data = get_test_data('all-rus')

    clf_svm = svm.SVC(kernel='linear', C=1)
    clf_logreg = linear_model.LogisticRegression(C=1)

    if alg == 'svm':
        clf = clf_svm
    if alg == 'log':
        clf = clf_logreg

    scores = cross_validation.cross_val_score(clf, test_data.data, test_data.target,
                                              cv=cv, n_jobs=-1)
    print scores
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()*2))

    print str(time.time() - start) + " sec"

classification('svm')
# classification('log')
