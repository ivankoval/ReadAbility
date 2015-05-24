import os
import nltk
import xml.etree.ElementTree as ElementTree
from ig_value import get_all_ig


def text_to_pos_eng(path_load, path_save):
    for grade in os.listdir(path_load):
        if grade != '.DS_Store':
            path_to_grade = path_load + grade + "/"
            for filename in os.listdir(path_to_grade):
                if filename != '.DS_Store':
                    with open(path_to_grade + filename, "r") as my_file:
                        data = my_file.read().replace('\n', '')
                        data = data.decode('utf-8')

                    text = []
                    for sent in nltk.sent_tokenize(data):
                        for chunk in nltk.pos_tag(nltk.word_tokenize(sent)):
                            if isinstance(chunk, tuple):
                                text.append(chunk[1])

                    if not os.path.exists(os.path.dirname(path_save + grade + "/" + filename)):
                        os.makedirs(os.path.dirname(path_save + grade + "/" + filename))
                    pos_file = open(path_save + grade + "/" + filename, 'w+')

                    for word in text:
                        pos_file.write("%s " % word)
                    pos_file.close()


def text_to_pos_rus(path_load, path_save):
    for grade in os.listdir(path_load):
        if grade != '.DS_Store':
            path_to_grade = path_load + grade + "/"
            for filename in os.listdir(path_to_grade):
                if filename != '.DS_Store':
                    with open(path_to_grade + filename, "r") as my_file:
                        data = my_file.read().replace('\n', '')
                    text = []
                    root = ElementTree.fromstring(data)

                    for word in root.iter('I-annotation'):
                        pos_tag = ''
                        for child in word:
                            if child.tag == 'value':
                                pos_tag = child[0].text
                        text.append(pos_tag)

                    if not os.path.exists(os.path.dirname(path_save + grade + "/" + filename)):
                        os.makedirs(os.path.dirname(path_save + grade + "/" + filename))
                    pos_file = open(path_save + grade + "/" + filename[:filename.index('.xml')] + '.txt', 'w+')
                    for word in text:
                        pos_file.write("%s " % word)
                    pos_file.close()


def text_to_ig_eng(path_load, grades, path_save):
    ig_words = get_all_ig(path_load, grades)

    for grade in grades:
        path_to_grade = path_load + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':
                with open(path_to_grade + filename, "r") as my_file:
                    data = my_file.read().replace('\n', '')
                    data = data.decode('utf-8')

                text = []
                for sent in nltk.sent_tokenize(data):
                    for chunk in nltk.pos_tag(nltk.word_tokenize(sent)):
                        if isinstance(chunk, tuple):
                            if chunk[0] in ig_words:
                                text.append(chunk[0])
                            else:
                                text.append(chunk[1])

                if not os.path.exists(os.path.dirname(path_save + grade + "/" + filename)):
                    os.makedirs(os.path.dirname(path_save + grade + "/" + filename))

                ig_file = open(path_save + grade + "/" + filename, 'w+')

                for word in text:
                    ig_file.write("%s " % word.encode('utf-8'))
                ig_file.close()


def text_to_ig_rus(path_load, grades, path_save):
    ig_words = get_all_ig(path_load, grades)
    for grade in grades:
        path_to_grade = path_load + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':
                with open(path_to_grade + filename, "r") as my_file:
                    data = my_file.read().replace('\n', '')
                text = []
                root = ElementTree.fromstring(data)

                for word in root.iter('I-annotation'):
                    start_word = 0
                    end_word = 0
                    pos_tag = ''

                    for child in word:
                        if child.tag == 'start':
                            start_word = int(child.text)
                        if child.tag == 'end':
                            end_word = int(child.text)
                        if child.tag == 'value':
                            pos_tag = child[0].text
                    text_word = root[0].text[start_word:end_word]
                    if text_word in ig_words:
                        text.append(text_word)
                    else:
                        text.append(pos_tag)

                    if not os.path.exists(os.path.dirname(path_save + grade + "/" + filename)):
                        os.makedirs(os.path.dirname(path_save + grade + "/" + filename))

                    ig_file = open(path_save + grade + "/" + filename[:filename.index('.xml')] + '.txt', 'w+')

                    for item in text:
                        ig_file.write("%s " % item.encode('utf-8'))
                    ig_file.close()

# text_to_pos_eng('/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/',
#                 '/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/pos/')

# text_to_pos_rus('/Users/Ivan/PycharmProject/ReadAbility/ApiData/pos/',
#                 '/Users/Ivan/PycharmProject/ReadAbility/DataSets/Russian/pos/')

text_to_ig_eng('/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/', ['K-1', '4-5', '9-10'],
                '/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/ig/')

# text_to_ig_rus('/Users/Ivan/PycharmProject/ReadAbility/ApiData/pos/', ['1', '3', '6', '9'],
#                 '/Users/Ivan/PycharmProject/ReadAbility/DataSets/Russian/ig/')

