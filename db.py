import sqlite3
from flask import current_app, g

def get_db():
    g.con = sqlite3.connect('blog.db')
    g.con.row_factory = sqlite3.Row
    return g.con

def init_db():
    con = get_db()
    with current_app.open_resource('schema.sql') as f:
        con.executescript(f.read().decode('utf8'))
    return con