from __future__ import division
import os
import string
import nltk
import re
const = r"bcdfghjklmnpqrstvwxyz"
vow = r'aeiou'


def total_words(text):
    exclude = set(string.punctuation)
    words = nltk.tokenize.word_tokenize(text)
    words = [word for word in words if word not in exclude]
    return words


def count_syllables(s):
    syl_count = 0
    qu = re.compile(r'qu')
    s = qu.sub('qw',s)

    ends = re.compile(r'(es$)|(que$)|(gue$)')
    s = ends.sub('',s)

    s = re.sub(r'^re',r'ren',s)
    s = re.sub(r'^gua',r'ga',s)
    s = re.sub(r'([aeiou])(l+e$)',r'\g<1>',s)
    (s,nsyl_count) = re.subn(r'([bcdfghjklmnpqrstvwxyz])(l+e$)',r'\g<1>',s)
    syl_count += nsyl_count


    s = re.sub(r'([aeiou])(ed$)',r'\g<1>',s)
    (s,nsyl_count) = re.subn(r'([bcdfghjklmnpqrstvwxyz])(ed$)',r'\g<1>',s)
    syl_count += nsyl_count

    endsp = re.compile(r'(ly$)|(ful$)|(ness$)|(ing$)|(est$)|(er$)|(ent$)|(ence$)')
    (s,nsyl_count) = endsp.subn(r'',s)
    syl_count += nsyl_count
    (s,nsyl_count) = endsp.subn(r'',s)
    syl_count += nsyl_count

    s = re.sub(r'(^y)([aeiou][aeiou]*)',r'\g<2>',s)
    s = re.sub(r'([aeiou])(y)',r'\g<1>t',s)
    (s,nsyl_count) = re.subn(r'(^y)([bcdfghjklmnpqrstvwxyz])',r'\g<2>',s)
    syl_count += nsyl_count
    syl_count += nsyl_count

    s = re.sub(r'aa+',r'a',s)
    s = re.sub(r'ee+',r'e',s)
    s = re.sub(r'ii+',r'i',s)
    s = re.sub(r'oo+',r'o',s)
    s = re.sub(r'uu+',r'u',s)

    dipthongs = re.compile(r'(ai)|(au)|(ea)|(ei)|(eu)|(ie)|(io)|(oa)|(oe)|(oi)|(ou)|(ue)|(ui)')
    s,nsyl_count = dipthongs.subn('',s)
    syl_count += nsyl_count

    if len(s)>3:
        s = re.sub(r'([bcdfghjklmnpqrstvwxyz])(e$)',r'\g<1>',s)

    s,nsyl_count = re.subn(r'[aeiouy]', '', s)
    syl_count += nsyl_count
    return syl_count


def total_sentences(text):
    sent = nltk.sent_tokenize(text)
    return len(sent)


# average number of syllables per word
def feature_one(text):
    words = total_words(text)
    syllables_sum = 0
    for word in words:
        syllables_sum += count_syllables(word)
    return syllables_sum/len(words)


# percentage of poly-syll. words per doc.
def feature_two(text):
    words = total_words(text)
    poly_syllables_words = 0
    for word in words:
        if count_syllables(word) > 1:
            poly_syllables_words += 1
    return poly_syllables_words/len(words)*100


# average number of poly-syll. words per sent.
def feature_three(text):
    words = total_words(text)
    poly_syllables_words = 0
    for word in words:
        if count_syllables(word) > 1:
            poly_syllables_words += 1
    return poly_syllables_words/total_sentences(text)


# average number of characters per word
def feature_four(text):
    words = total_words(text)
    characters_sum = 0
    for word in words:
        characters_sum += len(word)
    return characters_sum/len(words)


# Chall-Dale difficult words rate per doc.
def feature_five(text):
    path_difficult_words = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/DaleChallEasyWordList.txt"
    words = total_words(text)
    difficult_words_sum = 0

    with open(path_difficult_words, 'r') as f:
        difficult_words = f.readlines()

    for word in words:
        if word not in difficult_words:
            difficult_words_sum += 1
    return 0.0496 * len(words)/total_sentences(text) + 0.1579 * difficult_words_sum/len(words) * 100 + 3.6365


# average number of words per sentence
def feature_six(text):
    return len(total_words(text))/total_sentences(text)


# Flesch-Kincaid score
def feature_seven(text):
    words = total_words(text)
    syllables_sum = 0
    for word in words:
        syllables_sum += count_syllables(word)

    return 0.39 * len(words)/total_sentences(text) + 11.8 * syllables_sum/len(words) - 15.59


# total number of words per document
def feature_eight(text):
    return len(total_words(text))


def extract_features(path):
    with open(path, "r") as myfile:
        text = myfile.read().replace('\n', '')
        text = text.decode('utf-8')

    return [feature_one(text), feature_two(text), feature_three(text), feature_four(text),
            feature_five(text), feature_six(text), feature_seven(text), feature_eight(text)]


def get_test_data():
    grades = ['K-1', '4-5', '9-10']
    # grades = ['2-3', '6-8', '11-CCR']
    # grades = ['K-1', '2-3', '4-5', '6-8', '9-10', '11-CCR']
    path = "/Users/Ivan/PycharmProject/ReadAbility/DataSets/English/byGrade/"
    path_to_features = "/Users/Ivan/PycharmProject/ReadAbility/features/shallow_features_eng.txt"
    features_file = open(path_to_features, 'w+')

    for grade in grades:
        path_to_grade = path + grade + "/"
        for filename in os.listdir(path_to_grade):
            if filename != '.DS_Store':
                features = extract_features(path_to_grade + filename)
                for feature in features:
                    features_file.write(str(feature) + '\n')
                features_file.write(str(grade) + '\n')

    features_file.close()


get_test_data()