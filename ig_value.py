from __future__ import division

import math
import operator
import string
import nltk
from nltk.corpus import stopwords
from common_functions import prepare_dataset


def calc_entropy(x, y):
    if x == 0:
        return 0
    return -x/(x+y) * math.log(x/(x+y), 2)


def calc_ig_value(word, grades, dataset):
    entropy = 0
    entropy_with_word = 0
    entropy_without_word = 0

    for c in grades:
        tp = fp = fn = tn = 0

        for text in dataset:
            if text.grade == c:
                if word in text.data:
                    tp += 1
                else:
                    fn += 1
            else:
                if word in text.data:
                    fp += 1
                else:
                    tn += 1
        entropy += calc_entropy(tp + fn, fp + tn)
        entropy_with_word = calc_entropy(tp, fp)
        entropy_without_word = calc_entropy(fn, tn)

    num_text_with_word = 0
    for text in dataset:
        if word in text.data:
            num_text_with_word = +1

    prob_word = num_text_with_word / len(dataset)

    return entropy - prob_word * entropy_with_word - (1-prob_word) * entropy_without_word


def prepare_ig_candidates(dataset):
    ig_candidates = []
    fd = nltk.FreqDist()
    stops = stopwords.words('english')

    for text in dataset:
        for sent in nltk.sent_tokenize(text.data.lower()):
            for word in nltk.word_tokenize(sent):
                if word not in stops and word not in string.punctuation:
                    fd[word] += 1

    for word in fd:
        if fd[word] > 2:
            ig_candidates.append(word)
    return ig_candidates


def get_all_ig(path, grades):

    dataset = prepare_dataset(path, grades)
    words = prepare_ig_candidates(dataset)
    ig_words = dict()

    for word in words:
        ig_words[word] = calc_ig_value(word, grades, dataset)

    sorted_ig_words = sorted(ig_words.items(), key=operator.itemgetter(1), reverse=True)

    top_ig_words = list()
    for word in sorted_ig_words:
        if len(top_ig_words) < 1000:
            top_ig_words.append(word[0])
        else:
            break
    return top_ig_words


# path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/"
# grades = ['2-3', '6-8', '11-CCR']

# path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/Russian/dictant/"
# grades = ['1', '3', '6', '9']

# for word in get_all_ig(path, grades):
#     print word
