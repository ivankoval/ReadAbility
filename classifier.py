__author__ = 'IvanK'

from sklearn import svm
from sklearn import linear_model
from sklearn import tree
from sklearn import cross_validation
import numpy as np
from itertools import chain, combinations


def powerset(iterable):
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable( combinations(xs,n) for n in range(len(xs)+1) )


class TestData:
    data = []
    target = []

    def __init__(self):
        self.data = []
        self.target = []


def get_test_data(type, features_set):
    i = 0
    test_data = TestData()

    if type == 'ent_eng':
        with open("features.txt") as f:
            content = f.readlines()
        while i < len(content):
            test_data.data.append(np.array([content[i], content[i+1]], dtype=float))
            # test_data.target.append(np.array((content[i+2]), dtype=float))
            test_data.target.append((content[i+2]))
            i += 3

    if type == 'ent_rus':
        with open("features_rus.txt") as f:
            content = f.readlines()
        while i < len(content):
            test_data.data.append(np.array([content[i], content[i+1]], dtype=float))
            test_data.target.append(np.array((content[i+2]), dtype=float))
            i += 3

    if type == 'lm_eng':
        with open("features_lm.txt") as f:
            content = f.readlines()
        while i < len(content):
            arr = []
            for feature in features_set:
                arr.append(content[i+feature])
            test_data.data.append(np.array(arr, dtype=float))
            test_data.target.append((content[i+5]))
            i += 6

    if type == 'lm_rus':
        with open("features_lm_rus.txt") as f:
            content = f.readlines()
        while i < len(content):
            arr = []
            for feature in features_set:
                arr.append(content[i+feature])
            test_data.data.append(np.array(arr, dtype=float))
            test_data.target.append((content[i+5]))
            i += 6

    return test_data


def classification(type, features_set):
    cv = 3
    test_data = get_test_data(type, features_set)

    logreg = linear_model.LogisticRegression(C=1)
    # logreg = linear_model.LogisticRegression(C=1, penalty='l1')
    clf_svm = svm.SVC(kernel='linear', C=1)
    clf_tree = tree.DecisionTreeClassifier()

    scores = cross_validation.cross_val_score(clf_svm, test_data.data, test_data.target,
                                              cv=cv, n_jobs=-1)

    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

for items in list(powerset(set([0, 1, 2, 3, 4]))):
    if len(items) != 0:
        print items
        classification('lm_rus', items)