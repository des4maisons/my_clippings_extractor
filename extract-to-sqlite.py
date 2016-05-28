#!/usr/bin/env python3.5
import sys
import kindle_clippings_lexer
from kindle_clippings_parser import yacc
from sqlite_dumper import SqliteDumper

def get_content(fname):
    with open(fname) as f:
        content = f.read()
    return content

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('Usage: ' + sys.argv[0] + ' /path/to/my_clippings.txt', file=sys.stderr)
        sys.exit(1)
    data = yacc.parse(get_content(sys.argv[1]))
    d = SqliteDumper(file='foo.db')
    d.store(data)
