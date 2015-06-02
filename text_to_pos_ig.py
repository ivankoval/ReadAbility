import os
import nltk
import xml.etree.ElementTree as ElementTree
from ig_value import get_all_ig


def pos_eng(path_load, path_pos, path_word_pos):
    for grade in os.listdir(path_load):
        if grade != '.DS_Store':
            path_to_grade = path_load + grade + "/"
            for filename in os.listdir(path_to_grade):
                if filename != '.DS_Store':
                    with open(path_to_grade + filename, "r") as my_file:
                        data = my_file.read().replace('\n', '')
                        data = data.decode('utf-8')

                    text_pos = []
                    text_word_pos = []
                    for sent in nltk.sent_tokenize(data):
                        for chunk in nltk.pos_tag(nltk.word_tokenize(sent)):
                            if isinstance(chunk, tuple):
                                text_pos.append(chunk[1])
                                text_word_pos.append(chunk[0] + '_' + chunk[1])

                    if not os.path.exists(os.path.dirname(path_pos + grade + "/" + filename)):
                        os.makedirs(os.path.dirname(path_pos + grade + "/" + filename))
                    pos_file = open(path_pos + grade + "/" + filename, 'w+')

                    for word in text_pos:
                        pos_file.write("%s " % word)
                    pos_file.close()

                    if not os.path.exists(os.path.dirname(path_word_pos + grade + "/" + filename)):
                        os.makedirs(os.path.dirname(path_word_pos + grade + "/" + filename))
                    word_pos_file = open(path_word_pos + grade + "/" + filename, 'w+')

                    for word in text_word_pos:
                        word_pos_file.write("%s " % word.encode('utf-8'))
                    word_pos_file.close()


def pos_rus(path_load, path_pos, path_word_pos):
    path_to_api = '/Users/Ivan/PycharmProject/ReadAbility/ApiData/rus/pos/'
    for grade in os.listdir(path_load):
        if grade != '.DS_Store':
            path_to_grade = path_load + grade + "/"
            for filename in os.listdir(path_to_grade):
                if filename != '.DS_Store':

                    with open(path_to_api + grade + "/" + filename[:filename.index('.txt')] + '.xml', "r") as my_file:
                        data = my_file.read().replace('\n', '')
                    text_pos = []
                    text_word_pos = []

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
                        text_pos.append(pos_tag)

                        text_word = root[0].text[start_word:end_word]
                        text_word_pos.append(text_word + '_' + pos_tag)

                    if not os.path.exists(os.path.dirname(path_pos + grade + "/" + filename)):
                        os.makedirs(os.path.dirname(path_pos + grade + "/" + filename))
                    pos_file = open(path_pos + grade + "/" + filename, 'w+')
                    for word in text_pos:
                        pos_file.write("%s " % word)
                    pos_file.close()

                    if not os.path.exists(os.path.dirname(path_word_pos + grade + "/" + filename)):
                        os.makedirs(os.path.dirname(path_word_pos + grade + "/" + filename))
                    word_pos_file = open(path_word_pos + grade + "/" + filename, 'w+')
                    for word in text_word_pos:
                        word_pos_file.write("%s " % word.encode('utf-8'))
                    word_pos_file.close()


def ig_eng(path_load, path_ig):
    grades = os.listdir(path_load)
    grades.remove('.DS_Store')

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

                if not os.path.exists(os.path.dirname(path_ig + grade + "/" + filename)):
                    os.makedirs(os.path.dirname(path_ig + grade + "/" + filename))

                ig_file = open(path_ig + grade + "/" + filename, 'w+')

                for word in text:
                    ig_file.write("%s " % word.encode('utf-8'))
                ig_file.close()


def ig_rus(path_load, path_ig):
    path_to_api = '/Users/Ivan/PycharmProject/ReadAbility/ApiData/rus/pos/'
    grades = os.listdir(path_load)
    grades.remove('.DS_Store')
    ig_words = get_all_ig(path_load, grades)
    for grade in grades:
        path_to_grade = path_load + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':
                with open(path_to_api + grade + "/" + filename[:filename.index('.txt')] + '.xml', "r") as my_file:
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

                    if not os.path.exists(os.path.dirname(path_ig + grade + "/" + filename)):
                        os.makedirs(os.path.dirname(path_ig + grade + "/" + filename))
                    ig_file = open(path_ig + grade + "/" + filename, 'w+')

                    for item in text:
                        ig_file.write("%s " % item.encode('utf-8'))
                    ig_file.close()


path = '/Users/Ivan/PycharmProject/ReadAbility/DataSets_test/'

# pos_eng(path + 'eng/word/', path + 'eng/pos/', path + 'eng/word-pos/')
# pos_rus(path + 'rus/word/', path + 'rus/pos/', path + 'rus/word-pos/')

ig_eng(path + 'eng/word/', path + 'eng/ig/')
# ig_rus(path + 'rus/word/', path + 'rus/ig/')

# experiment! (change path to api)
# pos_rus(path + 'eng/word/', path + 'eng/pos_1/', path + 'eng/word-pos_1/')
