__author__ = 'IvanK'

from modis import texterra

t = texterra.TexterraAPI('3082674ef10c23ef8b191dfdb3005f5a7a77044d')
tags = t.posTaggingAnnotate('Hello World')