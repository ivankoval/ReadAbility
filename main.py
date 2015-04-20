__author__ = 'IvanK'

from sklearn import svm
from sklearn import linear_model
from sklearn import tree
from sklearn import cross_validation
import numpy as np


class TestData:
    data = []
    target = []

    def __init__(self):
        self.data = []
        self.target = []


def get_test_data(lang):
    i = 0
    test_data = TestData()

    if lang == 'eng':
        with open("features.txt") as f:
            content = f.readlines()
        while i < len(content):
            test_data.data.append(np.array([content[i], content[i+1]], dtype=float))
            test_data.target.append(content[i+2])
            i += 3

    if lang == 'rus':
        with open("features_rus.txt") as f:
            content = f.readlines()
        while i < len(content):
            test_data.data.append(np.array([content[i], content[i+1]], dtype=float))
            test_data.target.append(content[i+2])
            i += 3

    return test_data


def classification(lang):
    cv = 3
    test_data = get_test_data(lang)

    logreg = linear_model.LogisticRegression(C=1)
    # logreg = linear_model.LogisticRegression(C=1, penalty='l1')
    clf_svm = svm.SVC(kernel='linear', C=1)
    clf_tree = tree.DecisionTreeClassifier()

    scores = cross_validation.cross_val_score(logreg, test_data.data, test_data.target, cv=cv, n_jobs=-1)
    print scores
    print 'cv = ' + str(cv) + ' - scores: ' + str(scores.mean()) + ' +- ' + str(scores.std()*2)


classification('rus')