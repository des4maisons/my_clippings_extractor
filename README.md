# Installation

```
pyvenv-3.5 env  # or `virtualenv env` in python2
. env/bin/activate
pip install -r requirements.txt
```

# Usage

```
./extract-to-sqlite.py /path/to/kindle-notes [(-o|--output) sqlite.db]
```

where `/path/to/kindle-notes` is a text file in the following format:

```
<Title> (Authors)
[*|-|?] Your Highlight on page <page> | location <location1>-<location2> | Added on <Day>, <day> <Month> <Year> <HH:MM:SS>

<highlighted text>
==========
...
```

Eg:

```
Continuous Delivery (Jez Humble;David Farley)
- Your Highlight on page 216 | location 3300-3302 | Added on Saturday, 5 December 2015 18:50:48

Acceptance tests written without developer involvement also tend to be tightly coupled to the UI and thus brittle and badly factored, because the testers don’t have any insight into the UI’s underlying design and lack the skills to create abstraction layers or run acceptance tests against a public API.
==========
﻿Continuous Delivery (Jez Humble;David Farley)
- Your Highlight on page 269 | location 4110-4111 | Added on Saturday, 5 December 2015 19:40:02

Build In Traceability from Binaries to Version Control
==========
﻿Continuous Delivery (Jez Humble;David Farley)
- Your Highlight on page 272 | location 4162-4162 | Added on Saturday, 5 December 2015 19:47:08

use the build and deployment process as a guide to your collection of scripts.
==========
```
