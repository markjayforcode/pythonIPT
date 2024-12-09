import sqlite3

# Create or connect to the database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT,
            description TEXT)''')  # Fixed the closing parenthesis
conn.commit()

# Function to add an expense
def add_expense(date, amount, category, description):
    c.execute('''INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)''', 
              (date, amount, category, description))
    conn.commit()
