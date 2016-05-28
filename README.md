# Installation

```
make install
```

# Running tests

```
make test
```

# Usage

```
env/bin/python extract-to-sqlite.py --input /path/to/myclippings.txt --output /path/to/sqlite.db
```

Once you have done this, you can manipulate the data however you want:

```
$ sqlite3 sqlite.db
SQLite version 3.8.10.2 2015-05-20 18:17:19
Enter ".help" for usage hints.
sqlite> SELECT COUNT(*) FROM clippings WHERE TITLE LIKE 'continuous deliv%';
38
sqlite>
```

`myclippings.txt` should follow a format similar to:

```
Continuous Delivery (Jez Humble;David Farley)
- Your Highlight on page 216 | location 3300-3302 | Added on Saturday, 5 December 2015 18:50:48

Acceptance tests written without developer involvement also tend to be tightly coupled to the UI and thus brittle and badly factored, because the testers don’t have any insight into the UI’s underlying design and lack the skills to create abstraction layers or run acceptance tests against a public API.
==========
Continuous Delivery (Jez Humble;David Farley)
- Your Highlight on page 269 | location 4110-4111 | Added on Saturday, 5 December 2015 19:40:02

Build In Traceability from Binaries to Version Control
==========
Continuous Delivery (Jez Humble;David Farley)
- Your Highlight on page 272 | location 4162-4162 | Added on Saturday, 5 December 2015 19:47:08

use the build and deployment process as a guide to your collection of scripts.
==========
```
