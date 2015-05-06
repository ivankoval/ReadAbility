__author__ = 'Ivan'

import time
import os
import requests


def load_xml(path, case):

    with open(path, "r") as myfile:
        data = myfile.read().replace('\n', '')

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    api_key = '3082674ef10c23ef8b191dfdb3005f5a7a77044d'
    filtering = 'KEEPING'
    payload = {"text": data}

    if case == 'ent':
        class_ = 'named-entity'
        url = 'ru.ispras.texterra.core.nlp.pipelines.NETaggingPipeline'
    if case == 'pos':
        class_ = 'penn-pos'
        url = 'pos'

    r = requests.post('http://ApiData.ispras.ru/texterra/v3.1/nlp/' + url + '?apikey=' + api_key + '&filtering=' +
                      filtering + '&class=' + class_, data=payload, headers=headers)

    return r.text


def get_api_data(case):
    folders = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10-11']
    path_load = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/Russian/dictant/"

    if case == 'ent':
        path_save = "/Users/Ivan/PycharmProject/ReadAbility/ApiData/ent/"
    if case == 'pos':
        path_save = "/Users/Ivan/PycharmProject/ReadAbility/ApiData/pos/"

    for folder in folders:
        path_to_folder = path_load + folder + "/"
        for filename in os.listdir(path_to_folder):
            if filename != '.DS_Store':
                time.sleep(1)
                xml_data = load_xml(path_load + folder + '/' + filename, case)
                xml_file = open(path_save + folder + '/' + filename[:filename.index('.txt')] + '.xml', 'w+')
                xml_file.write(xml_data.encode('utf-8'))
                xml_file.close()


get_api_data('pos')