# TODO 1. percentage of named entities per document
# TODO 2. percentage of named entities per sentences ?
# TODO 3. percentage of overlapping nouns removed ???
# TODO 4. average number of remaining nouns per sentence ???
# TODO 5. percentage of named entities in total entities
# TODO 6. percentage of remaining nouns in total entities ??? 100 - prev

from __future__ import division
import nltk
import string
import collections
import os
from  sklearn import svm
from sklearn import cross_validation


class TestData:
    data = []
    target = []

    def __init__(self):
        self.data = []
        self.target = []


def total_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return len(words)


def total_sentences(text):
    sent = nltk.sent_tokenize(text)
    return len(sent)


def extract_entities(text):
    named_entities = []
    proper_nouns = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.chunk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)), binary=True):
            if isinstance(chunk, nltk.tree.Tree):
                if chunk.label() == 'NE':
                    for entity in chunk.leaves():
                        named_entities.append(entity[0])
            if isinstance(chunk, tuple):
                if chunk[1] == 'NNP':
                    proper_nouns.append(chunk[0])
    entities = collections.namedtuple('Entities', ['ne', 'pn'])
    return entities(len(named_entities), len(proper_nouns))


def extract_features(path):
    with open(path, "r") as myfile:
        data = myfile.read().replace('\n', '')
        data = data.decode('utf-8')

    ne = extract_entities(data).ne
    pn = extract_entities(data).pn
    tw = total_words(data)
    ts = total_sentences(data)
    feature1 = ne/tw*100
    feature2 = ne/ts*100
    feature5 = ne/(ne+pn)*100
    feature6 = pn/(ne+pn)*100

    return [feature1, feature2, feature5, feature6]


def get_test_data():
    grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
    path = r"C:\Users\IvanK\PycharmProjects\ReadAbility\DataSets\English\byGrade\\"

    test_data = TestData()

    for grade in grades:
        path_to_grade = path + grade + '\\'
        for filename in os.listdir(path_to_grade):
            features = extract_features(path_to_grade + filename)
            arr = []
            for feature in features:
                arr.append(feature)
            test_data.data.append(arr)
            arr = []
            test_data.target.append(grade)
    return test_data


def classification():
    test_data = get_test_data()
    clf = svm.SVC(kernel='linear', C=1)
    scores = cross_validation.cross_val_score(clf, test_data.data, test_data.target, cv = 5)
    print scores


classification()
