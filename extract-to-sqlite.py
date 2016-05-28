#!/usr/bin/env python3.5
import sys
import kindle_clippings_lexer
from kindle_clippings_parser import yacc
from sqlite_dumper import SqliteDumper
from argparse import ArgumentParser

def get_content(fname):
    with open(fname) as f:
        content = f.read()
    return content

def create_cli_parser():
    parser = ArgumentParser(description='Dump MyClippings.txt to SQLite')
    parser.add_argument(
        '--input',
        default='My Clipiings.txt',
        type=str,
        help='/path/to/MyClippings.txt',
    )
    parser.add_argument(
        '--output',
        default='sqlite.db',
        type=str,
        help='/path/to/output.db, a sqlite database',
    )
    return parser

if __name__ == '__main__':
    args = create_cli_parser().parse_args()
    data = yacc.parse(get_content(args.input))
    d = SqliteDumper(file=args.output)
    d.store(data)
