__author__ = 'IvanK'

import numpy as np
from sklearn import svm
from sklearn import datasets
from sklearn import cross_validation


# X = [[0, 0], [1, 1]]
# Y = [0, 1]
# clf = svm.SVC()
# clf.fit(X, Y)

iris = datasets.load_iris()
clf = svm.SVC(kernel='linear', C=1)
# scores = cross_validation.cross_val_score(clf, iris.data, iris.target, cv = 5)
print iris
