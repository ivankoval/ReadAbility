__author__ = 'IvanK'
import os


def file_sort_key(filename):
    index = filename.index('.')
    return int(filename[:index])


path = r"C:\Users\IvanK\Google Drive\isp\NIR\ReadAbility\DataSets\English\raw\test\\"
arr = []
num = 28
reverse = True

for filename in os.listdir(path):
    arr.append(filename)

arr.sort(key=file_sort_key, reverse=reverse)

for filename in arr:
    index = filename.index('.')
    os.rename(path + filename, path + str(int(filename[:index])+num) + '.txt')

