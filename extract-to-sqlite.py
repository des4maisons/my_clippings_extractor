#!/usr/bin/env python3.5
from pprint import PrettyPrinter
from datetime import datetime
import sys
import ply.lex as lex
import ply.yacc as yacc

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








start = 'clippings'

def p_empty(p):
    'empty :'
    pass

def p_clippings(p):
    '''
    clippings : clipping NEWLINE clippings
              | clipping
              | empty
    '''
    pass

def p_clipping_notequote(p):
    '''
    clipping : authorline NEWLINE locationline NEWLINE NEWLINE CONTENT NEWLINE CLIPPING_SEP
    '''
    p[0] = { **p[1], **p[3], 'content': p[6] }
    PrettyPrinter(indent=4).pprint(p[0])

def p_clipping_bookmark(p):
    '''
    clipping : authorline NEWLINE locationline NEWLINE NEWLINE NEWLINE CLIPPING_SEP
    '''
    p[0] = { **p[1], **p[3], 'content': '' }
    PrettyPrinter(indent=4).pprint(p[0])

def p_authorline(p):
    '''
    authorline : TITLE AUTHORS
    '''
    p[0] = {
        'title': p[1][:-1],
        'authors': p[2][:-1],
    }

def p_locationline_onpage(p):
    '''
    locationline : YOUR type ON_PAGE PAGE FIELD_SEP LOCATION_INTRO LOCATION FIELD_SEP datetime
    '''
    p[0] = {
        'type': p[2],
        'page': p[4],
        'location': p[7],
        'datetime': p[9],
    }

def p_locationline_loconly(p):
    '''
    locationline : YOUR type AT_LOCATION LOCATION FIELD_SEP datetime
    '''
    p[0] = {
        'type': p[2],
        'page': '',
        'location': p[4],
        'datetime': p[6],
    }

def p_type(p):
    '''
    type : BOOKMARK_TYPE
         | NOTE_TYPE
         | HIGHLIGHT_TYPE
    '''
    p[0] = p[1]

def p_datetime(p):
    '''
    datetime : ADDED_ON DAY_OF_WEEK COMMA DAY MONTH YEAR TIME
    '''
    p[0] = datetime.strptime(
        '%s %s %s %s' %(p[4].strip(), p[5].strip(), p[6].strip(), p[7].strip()),
        '%d %B %Y %H:%M:%S',  # 23 December 2015 22:36:59
    )

def p_error(p):
    print("Syntax error at '%s'" % p.value, file=sys.stderr)
    sys.exit(1)

def get_content(fname):
    with open(fname) as f:
        content = f.read()
    return content

def test_lexer(lexer):
    data = '''﻿Continuous Delivery (Jez Humble;David Farley)
- Your Highlight on page 205 | location 3134-3135 | Added on Saturday, 5 December 2015 18:46:33

The smoke test, or deployment test, is probably the most important test to write once you have a unit test suite up and running—indeed,
==========
﻿Continuous Delivery (Jez Humble;David Farley)
- Your Highlight on page 216 | location 3300-3302 | Added on Saturday, 5 December 2015 18:50:48

Acceptance tests written without developer involvement also tend to be tightly coupled to the UI and thus brittle and badly factored, because the testers don’t have any insight into the UI’s underlying design and lack the skills to create abstraction layers or run acceptance tests against a public API.
==========
﻿On Writing Well, 30th Anniversary Edition (William Zinsser)
- Your Bookmark on page 19 | location 288 | Added on Saturday, 19 December 2015 16:12:17


==========
Thinking in Systems (Donella H. Meadows)
- Your Highlight on page 153 | location 2332-2334 | Added on Friday, 13 May 2016 09:04:21

You have the problem of wrong goals when you find something stupid happening “because it’s the rule.” You have the problem of rule beating when you find something stupid happening because it’s the way around the rule.
==========
'''
    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('Usage: ' + sys.argv[0] + ' /path/to/my_clippings.txt', file=sys.stderr)
        sys.exit(1)

    lex.lex(debug=1)
    yacc.yacc()
    content = get_content(sys.argv[1])
    yacc.parse(content)
    #test_lexer(lex.lex(debug=1), content)
