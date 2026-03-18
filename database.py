import sqlite3

def init_db():
    conn = sqlite3.connect("cinema_db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   director TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

def get_connection():
    return sqlite3.connect("cinema_db")