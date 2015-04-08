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


grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
path = r"C:\Users\IvanK\PycharmProjects\ReadAbility\DataSets\English\byGrade\\"

for grade in grades:
    pathToGrade = path + grade + '\\'
    for filename in os.listdir(pathToGrade):
        features = extract_features(pathToGrade + filename)
        for feature in features:
            print str(feature) + ", ",
        print grade