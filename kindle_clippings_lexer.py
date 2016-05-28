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
    'AUTHORS_START',
    'AUTHORS',
    'AUTHORS_END',
    'YOUR',
    'HIGHLIGHT_TYPE',
    'BOOKMARK_TYPE',
    'NOTE_TYPE',
    'ON_PAGE',
    'PAGE',
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
    r'\ufeff'
    pass

t_titleline_TITLE = '.+(?=\ \([^)]+\)\n)' # up to last set of parentheses
t_titleline_AUTHORS = '[^(]+(?=\)\n)' # inside last set of parentheses
t_titleline_AUTHORS_START = '\ \((?=[^\(]\n)' # opening of last set of parenthesis
t_titleline_AUTHORS_END = '\)(?=\n)' # closing of last set of parenthesis

t_locationline_YOUR = '-\ Your'
t_locationline_HIGHLIGHT_TYPE = 'Highlight'
t_locationline_BOOKMARK_TYPE = 'Bookmark'
t_locationline_NOTE_TYPE = 'Note'
t_locationline_ON_PAGE = 'on\ page'
t_locationline_PAGE = '(?<=' + t_locationline_ON_PAGE + '\ )\d+'
t_locationline_LOCATION_INTRO = 'at\ location|location'
t_locationline_LOCATION = '(?<=location\ )\d+(-\d+)?'
t_locationline_FIELD_SEP = r'\|'
t_locationline_ADDED_ON = 'Added\ on'
t_locationline_DAY_OF_WEEK = 'Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday'
t_locationline_DAY = r'(?<=,\ )\d\d?(?=\ )'
t_locationline_COMMA = ','
t_locationline_YEAR = r'(?<=\ )\d\d\d\d(?=\ )'
t_locationline_MONTH = 'January|February|March|April|May|June|July|August|September|October|November|December'
t_locationline_TIME = r'\d\d:\d\d:\d\d'

def t_locationline_SPACE(t):
    '\ '
    pass

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
