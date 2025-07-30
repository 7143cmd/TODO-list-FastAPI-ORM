import sqlite3

def INSERT_INTO(UserPassword, CachedPassword, UserLogin):
    with sqlite3.connect("log.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO passWRD(UserLogin, 
                       UserPassword, 
                       CachedPassword)
                       VALUES(
                       ?,
                       ?,
                       ?)
                       """, (UserLogin, UserPassword, CachedPassword))
        conn.commit()

def DATABASE_CONNECT():
    conn = sqlite3.connect("log.db")
    conn.row_factory = sqlite3.Row
    return conn