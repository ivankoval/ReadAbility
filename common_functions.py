__author__ = 'Ivan'
import os
import string
import nltk


class Text:
    def __init__(self, name, grade, data):
        self.name = name
        self.grade = grade
        self.data = data


def prepare_dataset(path, grades):
    dataset = []
    for grade in grades:
        path_to_grade = path + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':
                with open(path_to_grade + filename, "r") as my_file:
                    data = my_file.read().replace('\n', '')
                    data = data.decode('utf-8')
                text = Text(filename, grade, data)
                dataset.append(text)
    return dataset


def get_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return words


def total_sentences(text):
    sent = nltk.sent_tokenize(text)
    return len(sent)