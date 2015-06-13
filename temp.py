# -*- coding: utf-8 -*-
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

p = morph.parse(u'стали')
for var in p:
    print var.tag.case