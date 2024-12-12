import sqlite3

def migrate_database():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    
    try:
        # Create backup of existing expenses
        c.execute("CREATE TABLE IF NOT EXISTS expenses_backup AS SELECT * FROM expenses")
        
        # Drop existing expenses table
        c.execute("DROP TABLE IF EXISTS expenses")
        
        # Create new expenses table with user_id
        c.execute('''CREATE TABLE expenses
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     date TEXT NOT NULL,
                     amount TEXT NOT NULL,
                     category TEXT NOT NULL,
                     description TEXT,
                     user_id TEXT NOT NULL,
                     FOREIGN KEY (user_id) REFERENCES users(username))''')
        
        # Copy data from backup with default user_id
        c.execute("INSERT INTO expenses (date, amount, category, description, user_id) SELECT date, amount, category, description, 'admin' FROM expenses_backup")
        
        # Drop backup table
        c.execute("DROP TABLE expenses_backup")
        
        conn.commit()
        print("Database migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {str(e)}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database() 