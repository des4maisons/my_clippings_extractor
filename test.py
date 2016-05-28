from kindle_clippings_lexer import lexer
from kindle_clippings_parser import yacc
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

def test_tokenize():
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break

def test_parse():
    yacc.parse(data)
