import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('expenses.db', isolation_level=None)
    try:
        yield conn
    finally:
        conn.close()

def create_tables():
    with get_db_connection() as conn:
        c = conn.cursor()
        
        # Create users table if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY,
                     password TEXT NOT NULL)''')
        
        # Create expenses table with user_id
        c.execute('''CREATE TABLE IF NOT EXISTS expenses
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     date TEXT NOT NULL,
                     amount TEXT NOT NULL,
                     category TEXT NOT NULL,
                     description TEXT,
                     user_id TEXT NOT NULL,
                     FOREIGN KEY (user_id) REFERENCES users(username)
                     ON DELETE CASCADE)''')

def add_expense(date, amount, category, description, user_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("BEGIN TRANSACTION")
            c.execute("""INSERT INTO expenses 
                        (date, amount, category, description, user_id) 
                        VALUES (?, ?, ?, ?, ?)""",
                     (date, amount, category, description, user_id))
            c.execute("COMMIT")
            return True
        except Exception as e:
            c.execute("ROLLBACK")
            print(f"Error adding expense: {e}")
            return False

def get_user_expenses(user_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("""SELECT * FROM expenses 
                        WHERE user_id = ? 
                        ORDER BY date DESC""", (user_id,))
            return c.fetchall()
        except Exception as e:
            print(f"Error getting expenses: {e}")
            return []

def verify_user_session(user_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (user_id,))
        return c.fetchone() is not None
