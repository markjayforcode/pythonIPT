from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from session import UserSession

def create_user_table():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class AuthWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        create_user_table()
        
        # Center the window
        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Get the window width and height
        window_width = 400  # Adjust this to your login window width
        window_height = 300  # Adjust this to your login window height
        
        # Calculate position coordinates
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        
        # Set the position of the window to the center of the screen
        root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
        
        self.show_login()
    
    def show_login(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = Frame(self.root)
        frame.pack(pady=20)
        
        Label(frame, text="Login", font=("Arial", 20, "bold")).pack(pady=10)
        
        Label(frame, text="Username:", font=("Arial", 10)).pack()
        self.username = Entry(frame, font=("Arial", 10))
        self.username.pack(pady=5)
        
        Label(frame, text="Password:", font=("Arial", 10)).pack()
        self.password = Entry(frame, font=("Arial", 10), show="*")
        self.password.pack(pady=5)
        
        Button(frame, text="Login", command=self.login, 
               bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=10)
        
        Button(frame, text="Create Account", command=self.show_signup,
               bg="#2196F3", fg="white", font=("Arial", 10)).pack()
    
    def show_signup(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = Frame(self.root)
        frame.pack(pady=20)
        
        Label(frame, text="Create Account", font=("Arial", 20, "bold")).pack(pady=10)
        
        Label(frame, text="Username:", font=("Arial", 10)).pack()
        self.new_username = Entry(frame, font=("Arial", 10))
        self.new_username.pack(pady=5)
        
        Label(frame, text="Password:", font=("Arial", 10)).pack()
        self.new_password = Entry(frame, font=("Arial", 10), show="*")
        self.new_password.pack(pady=5)
        
        Label(frame, text="Confirm Password:", font=("Arial", 10)).pack()
        self.confirm_password = Entry(frame, font=("Arial", 10), show="*")
        self.confirm_password.pack(pady=5)
        
        Button(frame, text="Sign Up", command=self.signup,
               bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=10)
        
        Button(frame, text="Back to Login", command=self.show_login,
               bg="#2196F3", fg="white", font=("Arial", 10)).pack()
    
    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            
            # Verify user credentials
            c.execute("SELECT password FROM users WHERE username=?", (username,))
            result = c.fetchone()
            
            if result and result[0] == hash_password(password):
                # Set user session
                UserSession.clear()  # Clear any existing session
                UserSession.set_user(username)
                
                # Verify session was set
                if UserSession.get_user() != username:
                    raise Exception("Failed to initialize user session")
                    
                self.root.destroy()
                self.start_main_app()
            else:
                messagebox.showerror("Error", "Invalid username or password")
            
        except Exception as e:
            messagebox.showerror("Login Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()
    
    def signup(self):
        username = self.new_username.get()
        password = self.new_password.get()
        confirm = self.confirm_password.get()
        
        if not username or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        
        # Check if username already exists
        c.execute("SELECT username FROM users WHERE username=?", (username,))
        if c.fetchone():
            conn.close()
            messagebox.showerror("Error", "Username already exists")
            return
        
        # Create new user
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login()
    
    def start_main_app(self):
        root = Tk()
        
        # Center the main expense tracker window
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        
        from main import initialize_main_window
        initialize_main_window(root) 