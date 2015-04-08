__author__ = 'IvanK'

from sklearn import svm

X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = svm.SVC()
clf.fit(X, Y)
