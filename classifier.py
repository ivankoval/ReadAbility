__author__ = 'IvanK'

from sklearn import svm
from sklearn import linear_model
from sklearn import tree
from sklearn import cross_validation
import numpy as np
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
        test_data.target.append(text_feature['grade'])
        test_data.data.append(np.array(text_feature['features'], dtype=float))

    return test_data


def classification():
    cv = 10
    test_data = get_test_data('lm-eng')

    logreg = linear_model.LogisticRegression(C=1)
    clf_svm = svm.SVC(kernel='linear', C=1)
    clf_tree = tree.DecisionTreeClassifier()

    scores = cross_validation.cross_val_score(clf_svm, test_data.data, test_data.target,
                                              cv=cv, n_jobs=-1)

    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


classification()