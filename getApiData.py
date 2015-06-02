__author__ = 'Ivan'

import time
import os
import requests


def load_xml(path, type_):

    with open(path, "r") as myfile:
        data = myfile.read().replace('\n', '')

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    api_key = '3082674ef10c23ef8b191dfdb3005f5a7a77044d'
    filtering = 'KEEPING'
    payload = {"text": data}

    if type_ == 'ent':
        class_ = 'named-entity'
        url = 'ru.ispras.texterra.core.nlp.pipelines.NETaggingPipeline'
    if type_ == 'pos':
        class_ = 'penn-pos'
        url = 'pos'

    r = requests.post('http://api.ispras.ru/texterra/v3.1/nlp/' + url + '?apikey=' + api_key + '&filtering=' +
                      filtering + '&class=' + class_, data=payload, headers=headers)
    return r.text


def get_api_data(path_load, path_save, grades, type_):

    for grade in grades:
        path_to_folder = path_load + grade + "/"
        for filename in os.listdir(path_to_folder):
            if filename != '.DS_Store':
                time.sleep(1)
                xml_data = load_xml(path_load + grade + '/' + filename, type_)
                xml_file = open(path_save + grade + '/' + filename[:filename.index('.txt')] + '.xml', 'w+')
                xml_file.write(xml_data.encode('utf-8'))
                xml_file.close()


def run(lang, type_):
    path_save = "/Users/Ivan/PycharmProject/ReadAbility/ApiData/"

    if lang == 'eng':
        grades = ['2-3', '4-5', '6-8', '9-10', '11-CCR']
        # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
        path_load = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/English/byGrade/"
    if lang == 'rus':
        grades = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10-11']
        path_load = "/Users/Ivan/PycharmProject/ReadAbility/DataSets_raw/Russian/dictant/"

    get_api_data(path_load, path_save + lang + '/' + type_ + '/', grades, type_)


run('eng', 'pos')
