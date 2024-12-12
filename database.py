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
        
        # Create users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY,
                     password TEXT NOT NULL,
                     monthly_budget REAL DEFAULT 0)''')
        print("Users table created or already exists.")
        
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
        print("Expenses table created or already exists.")



def add_monthly_budget_column():
    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            # Add the column if it doesn't already exist
            c.execute('''ALTER TABLE users ADD COLUMN monthly_budget REAL DEFAULT 0''')
            print("monthly_budget column added successfully.")
        except Exception as e:
            print(f"Error adding monthly_budget column: {e}")



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

def update_user_budget(user_id, budget):
    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("UPDATE users SET monthly_budget = ? WHERE username = ?", (budget, user_id))
            conn.commit()  # Ensure the changes are committed to the database
            return True
        except Exception as e:
            print(f"Error updating budget: {e}")
            return False


def get_user_budget(user_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT monthly_budget FROM users WHERE username = ?", (user_id,))
        result = c.fetchone()
        return result[0] if result else 0
