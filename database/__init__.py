import sqlite3

def get_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_tables():
    conn = get_db()
    c = conn.cursor()
    with open('database/schema.sql', 'r') as f:
        c.executescript(f.read())
    conn.commit()
    conn.close()
