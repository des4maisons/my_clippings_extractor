#!/usr/bin/env python3.5
from pprint import PrettyPrinter
from datetime import datetime
import sys
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'BOM',
    'TITLE',
    'AUTHOR_START',
    'AUTHOR',
    'AUTHOR_SEP',
    'AUTHOR_END',
    'LOCATION_LINE_START',
    'TYPE',
    'ON_PAGE',
    'PAGE',
    'FIELD_SEP',
    'AT_LOCATION',
    'LOCATION_INTRO',
    'LOCATION_RANGE',
    'ADDED_ON',
    'DAY',
    'COMMA',
    'DATE',
    'MONTH',
    'YEAR',
    'TIME',
    'CONTENT',
    'NEWLINE',
    'CLIPPING_SEP',
)

t_BOM = "\xfe\xff"
t_TITLE = r'^.+'
t_AUTHOR_START = r' \('
t_AUTHOR = r'.+?'
t_AUTHOR_SEP = ';'
t_AUTHOR_END = r'\)'
t_CLIPPING_SEP = r'^==========$'
t_LOCATION_LINE_START = '- Your'
t_TYPE = r'Note|Bookmark|Highlight'
t_ON_PAGE = 'on page'
t_PAGE = r'\d+'
t_FIELD_SEP = r'\|'
t_AT_LOCATION = 'at location'
t_LOCATION_INTRO = 'location'
t_LOCATION_RANGE = r'\d+-\d+'
t_ADDED_ON = 'Added on'
t_DAY = r'Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday'
t_COMMA = ','
t_DATE = r'\d\d?'
t_MONTH = r'January|February|March|April|May|June|July|August|September|October|November|December'
t_YEAR = r'\d\d\d\d'
t_TIME = r'\d\d:\d\d:\d\d'
t_CONTENT = r'^.+$'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    sys.exit(1)

def p_clipping_notequote(p):
    '''
    clipping : author_line NEWLINE location_line NEWLINE NEWLINE CONTENT NEWLINE CLIPPING_SEP
    '''
    p[0] = { **p[1], **p[3], 'content': p[6] }
    PrettyPrinter(indent=4).pprint(p[0])

def p_clipping_bookmark(p):
    '''
    clipping : author_line NEWLINE location_line NEWLINE NEWLINE NEWLINE CLIPPING_SEP
    '''
    p[0] = { **p[1], **p[3], 'content': '' }
    PrettyPrinter(indent=4).pprint(p[0])

def p_bom_author_line(p):
    '''
    author_line : BOM TITLE AUTHOR_START authors AUTHOR_END
    '''
    p[0] = {
        'title': p[2],
        'authors': p[4],
    }

def p_author_line(p):
    '''
    author_line : TITLE AUTHOR_START authors AUTHOR_END
    '''
    p[0] = {
        'title': p[1],
        'authors': p[3],
    }

def p_authors_one(p):
    '''
    authors : AUTHOR
    '''
    p[0] = p[1]

def p_authors_many(p):
    '''
    authors : authors AUTHOR_SEP authors
    '''
    p[0] = p[1] + p[2]

def p_location_line(p):
    '''
    location_line : LOCATION_LINE_START TYPE ON_PAGE PAGE FIELD_SEP LOCATION_INTRO LOCATION_RANGE FIELD_SEP datetime
                  | LOCATION_LINE_START TYPE AT_LOCATION LOCATION_RANGE FIELD_SEP datetime
    '''
    p[0] = {
        'type': p[2],
        'page': p[4],
        'location': p[6],
        'datetime': p[8],
    }


def p_datetime(p):
    '''
    datetime : ADDED_ON DAY COMMA DATE MONTH YEAR TIME
    '''
    p[0] = datetime.strptime(
        '%d %B %Y %H:%M:%S',  # 23 December 2015 22:36:59
        '%s %s %s %s' %(p[4], p[6], p[8], p[10])
    )

def p_error(p):
    print("Syntax error at '%s'" % p.value, file=sys.stderr)
    sys.exit(1)

def parse(fname):
    with open(fname) as f:
        content = f.read()
    yacc.parse(content)

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('Usage: ' + sys.argv[0] + ' /path/to/my_clippings.txt', file=sys.stderr)
        sys.exit(1)
    lex.lex()
    yacc.yacc()
    parse(sys.argv[1])

