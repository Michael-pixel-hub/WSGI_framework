import sqlite3

connect = sqlite3.connect('patterns.sqlite')
cur = connect.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
connect.close()