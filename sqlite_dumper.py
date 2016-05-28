import sqlite3

class SqliteDumper(object):
    def __init__(self, file=':memory:'):
        self.conn = sqlite3.connect(file)
        self.initialise()

    def initialise(self):
        self.conn.execute('''
            create table if not exists clippings (
                title,
                authors,
                page,
                location,
                type,
                content,
                datetime
            )
        ''')

    def store(self, data):
        self.conn.executemany('''
            INSERT INTO clippings (
                title,
                authors,
                page,
                location,
                type,
                content,
                datetime
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?
            )
        ''', map(lambda c: (
                c['title'],
                c['authors'],
                c['page'],
                c['location'],
                c['type'],
                c['content'],
                c['datetime'],
            ), data)
        )
        self.conn.commit()

