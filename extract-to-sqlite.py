#!/usr/bin/env python3.5
import sys
import kindle_clippings_lexer
from kindle_clippings_parser import yacc
from pprint import PrettyPrinter

def get_content(fname):
    with open(fname) as f:
        content = f.read()
    return content

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('Usage: ' + sys.argv[0] + ' /path/to/my_clippings.txt', file=sys.stderr)
        sys.exit(1)

    PrettyPrinter(indent=4).pprint(yacc.parse(get_content(sys.argv[1])))
