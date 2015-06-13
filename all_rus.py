# -*- coding: utf-8 -*-
import csv
from pymongo import MongoClient


def get_test_data():
    client = MongoClient('mongodb://localhost:27017/')
    features_collection = client.features['all-rus']
    features_collection.drop()

    path = "/Users/Ivan/PycharmProject/ReadAbility/all_no.csv"
    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile,  delimiter=";")
        for row in spamreader:
            i = 0
            features = list()
            for val in row:
                if i == 0:
                    if val == "":
                        break
                    grade = float(val)

                i += 1
                val = val.decode('utf-8')
                val.replace(u'\xc2', u'')
                val.replace(u'\xa0', u'')
                features.append(float(val))
            if len(features) != 0:
                print features
                text_features = {"grade": grade, "features": features}
                features_collection.insert_one(text_features)

get_test_data()



