# -*- coding: utf-8 -*-
__author__ = 'Ivan'

from itertools import chain, combinations


def powerset(iterable):
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable( combinations(xs,n) for n in range(len(xs)+1) )

print list(powerset(set([0, 1, 2, 3, 4])))