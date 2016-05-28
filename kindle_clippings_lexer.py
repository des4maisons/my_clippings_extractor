import ply.lex as lex

states = (
   ('titleline','exclusive'),
   ('locationline','exclusive'),
   ('contentline','exclusive'),
   ('separatorline','exclusive'),
   ('blankline','exclusive'),
)

tokens = (
    'TITLE',
    'AUTHORS',
    'YOUR',
    'HIGHLIGHT_TYPE',
    'BOOKMARK_TYPE',
    'NOTE_TYPE',
    'ON_PAGE',
    'PAGE',
    'AT_LOCATION',
    'LOCATION_INTRO',
    'LOCATION',
    'FIELD_SEP',
    'ADDED_ON',
    'DAY_OF_WEEK',
    'DAY',
    'COMMA',
    'YEAR',
    'MONTH',
    'TIME',
    'CONTENT',
    'NEWLINE',
    'CLIPPING_SEP',
)

def t_titleline_BOM(t):
    # the byte order mark sometimes appears before a clipping.
    # Ignore it.
    '﻿'
    pass

t_titleline_TITLE = r'.+\(' # up to last set of parentheses
t_titleline_AUTHORS = r'[^(]+\)' # inside last set of parentheses

t_locationline_YOUR = '-\sYour\s'
t_locationline_HIGHLIGHT_TYPE = 'Highlight'
t_locationline_BOOKMARK_TYPE = 'Bookmark'
t_locationline_NOTE_TYPE = 'Note'
t_locationline_ON_PAGE = '\son\spage\s'
t_locationline_PAGE = '(?<=' + t_locationline_ON_PAGE + ' )\d+'
t_locationline_AT_LOCATION = '\sat\slocation\s'
t_locationline_LOCATION_INTRO = 'location\s'
t_locationline_LOCATION = '(?<=location\s)\d+(-\d+)?'
t_locationline_FIELD_SEP = r'\s\|\s'
t_locationline_ADDED_ON = 'Added\son\s'
t_locationline_DAY_OF_WEEK = 'Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday'
t_locationline_DAY = r'(?<=,\s)\d\d?\s'
t_locationline_COMMA = ',\s'
t_locationline_YEAR = r'\s\d\d\d\d\s'
t_locationline_MONTH = 'January|February|March|April|May|June|July|August|September|October|November|December'
t_locationline_TIME = r'\d\d:\d\d:\d\d'

t_contentline_CONTENT = r'.+'

t_separatorline_CLIPPING_SEP = r'=========='

def t_ANY_NEWLINE(t):
    r'\n'
    t.lexer.lineno += t.value.count("\n")
    if t.lexer.lexstate == 'titleline':
        t.lexer.begin('locationline')
    elif t.lexer.lexstate == 'locationline':
        t.lexer.begin('blankline')
    elif t.lexer.lexstate == 'blankline':
        t.lexer.begin('contentline')
    elif t.lexer.lexstate == 'contentline':
        t.lexer.begin('separatorline')
    elif t.lexer.lexstate == 'separatorline':
        t.lexer.begin('titleline')
    return t

lexer = lex.lex()
lexer.begin('titleline')
