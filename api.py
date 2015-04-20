# -*- coding: utf-8 -*-
from __future__ import division
import requests
import xml.etree.ElementTree as ET
import nltk
import string
import os


def total_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return len(words)


def total_sentences(text):
    sent = nltk.sent_tokenize(text)
    return len(sent)


def extract_entities_api(text):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    api_key = '3082674ef10c23ef8b191dfdb3005f5a7a77044d'
    filtering = 'KEEPING'
    class_ = 'named-entity'
    payload = {"text": text}
    r = requests.post('http://api.ispras.ru/texterra/v3.1/nlp/ru.ispras.texterra.core.nlp.pipelines.NETaggingPipeline?apikey=' + api_key + '&filtering=' +
                      filtering + '&class=' + class_, data=payload, headers=headers)
    xml = r.text
    xml_file = open('api.xml', 'w+')
    xml_file.write(xml.encode('utf-8'))
    xml_file.close()
    tree = ET.parse('api.xml')
    root = tree.getroot()
    count = 0
    for value in root.iter('value'):
        count += 1
    return count


def extract_features(path):
    with open(path, "r") as myfile:
        data = myfile.read().replace('\n', '')
        data = data.decode('utf-8')

    ne = extract_entities_api(data)
    tw = total_words(data)
    ts = total_sentences(data)
    feature1 = ne/tw*100
    feature2 = ne/ts*100

    return [feature1, feature2]


def get_test_data():
    grades = ['1', '3', '4', '6', '8', '10', '11', '17']
    # grades = ['3']
    path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/Russian/textsbygrade/"
    features_file = open('features_rus.txt', 'w+')

    for grade in grades:
        path_to_grade = path + grade + "/"
        for filename in os.listdir(path_to_grade):
            features = extract_features(path_to_grade + filename)
            for feature in features:
                features_file.write(str(feature) + '\n')
            features_file.write(str(grade) + '\n')

    features_file.close()


get_test_data()