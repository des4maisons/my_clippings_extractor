import sys
import ply.yacc as yacc
from kindle_clippings_lexer import tokens
from datetime import datetime

start = 'clippings'

def p_empty(p):
    'empty :'
    pass

def p_clippings_multi(p):
    '''
    clippings : clipping NEWLINE clippings
    '''
    p[0] = [p[1]] + p[3]

def p_clippings_one(p):
    '''
    clippings : clipping
    '''
    p[0] = [p[1]]

def p_clippings_empty(p):
    '''
    clippings : empty
    '''
    p[0] = []

def p_clipping_notequote(p):
    '''
    clipping : authorline NEWLINE locationline NEWLINE NEWLINE CONTENT NEWLINE CLIPPING_SEP
    '''
    p[0] = { **p[1], **p[3], 'content': p[6] }

def p_clipping_bookmark(p):
    '''
    clipping : authorline NEWLINE locationline NEWLINE NEWLINE NEWLINE CLIPPING_SEP
    '''
    p[0] = { **p[1], **p[3], 'content': '' }

def p_authorline(p):
    '''
    authorline : TITLE AUTHORS_START AUTHORS AUTHORS_END
    '''
    p[0] = {
        'title': p[1],
        'authors': p[3],
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
    locationline : YOUR type LOCATION_INTRO LOCATION FIELD_SEP datetime
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
        '%s %s %s %s' %(p[4], p[5], p[6], p[7]),
        '%d %B %Y %H:%M:%S',  # 23 December 2015 22:36:59
    )

def p_error(p):
    print("Syntax error at '%s'" % p.value, file=sys.stderr)
    sys.exit(1)

yacc.yacc()
