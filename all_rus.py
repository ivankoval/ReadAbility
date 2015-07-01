# -*- coding: utf-8 -*-
import csv
from pymongo import MongoClient


def get_test_data():
    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['all-rus']
    features_collection.drop()

    path = "/Users/Ivan/PycharmProject/ReadAbility/all.csv"
    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile,  delimiter=";")
        for row in spamreader:
            i = 0
            features = list()
            for val in row:
                if val == "":
                    break

                if i == 0:
                    grade = str(val)
                else:
                    val = val.decode('utf-8')
                    val.replace(u'\xc2', u'')
                    val.replace(u'\xa0', u'')
                    features.append(float(val))
                i += 1
            if len(features) != 0:
                text_features = {"grade": grade, "features": features}
                print text_features
                features_collection.insert_one(text_features)

get_test_data()
