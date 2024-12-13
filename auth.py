from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from session import UserSession
from PIL import Image, ImageTk


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
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        create_user_table()
        
        # Center the window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Get the window width and height
        window_width = 400
        window_height = 550
        
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
        frame.pack(expand=True)
        
        # Title frame with logo3 and login text in vertical arrangement
        title_frame = Frame(frame)
        title_frame.pack(pady=(0, 5))
        
        # Center container for logo3
        logo_container = Frame(title_frame, width=400, height=261)
        logo_container.grid(row=0, column=0, columnspan=2)
        logo_container.grid_propagate(False)
        
        # Load and display logo3.png with specific size using PIL
        try:
            logo3_pil = Image.open("logo3.png")
            logo3_pil = logo3_pil.resize((321, 261), Image.LANCZOS)
            logo3_img = ImageTk.PhotoImage(logo3_pil)
            logo3_label = Label(logo_container, image=logo3_img)
            logo3_label.image = logo3_img
            logo3_label.place(x=60, y=30)
        except Exception as e:
            print(f"Error loading logo3.png: {e}")
        
        Label(title_frame, text="Login", font=("Arial", 20, "bold")).grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Content frame for username, password, and buttons
        content_frame = Frame(frame)
        content_frame.pack(pady=(0, 40))
        
        # Username row
        username_frame = Frame(content_frame)
        username_frame.pack(pady=10)
        
        try:
            logo_img = PhotoImage(file="logo.png")
            logo_img = logo_img.subsample(int(logo_img.width()/22), int(logo_img.height()/27))
            logo_label = Label(username_frame, image=logo_img)
            logo_label.image = logo_img
            logo_label.pack(side=LEFT, padx=5)
        except Exception as e:
            print(f"Error loading logo.png: {e}")
        
        username_container = Frame(username_frame)
        username_container.pack(side=LEFT)
        Label(username_container, text="Username:", font=("Arial", 10)).pack(side=LEFT, padx=(0,5))
        self.username = Entry(username_container, font=("Arial", 10))
        self.username.pack(side=LEFT)
        
        # Password row
        password_frame = Frame(content_frame)
        password_frame.pack(pady=10)
        
        try:
            logo2_img = PhotoImage(file="logo2.png")
            logo2_img = logo2_img.subsample(int(logo2_img.width()/22), int(logo2_img.height()/27))
            logo2_label = Label(password_frame, image=logo2_img)
            logo2_label.image = logo2_img
            logo2_label.pack(side=LEFT, padx=5)
        except Exception as e:
            print(f"Error loading logo2.png: {e}")
        
        password_container = Frame(password_frame)
        password_container.pack(side=LEFT)
        Label(password_container, text="Password:", font=("Arial", 10)).pack(side=LEFT, padx=(0,5))
        self.password = Entry(password_container, font=("Arial", 10), show="*")
        self.password.pack(side=LEFT)
        
        # Buttons
        Button(content_frame, text="Login", command=self.login, 
               bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=10)
        
        Button(content_frame, text="Create Account", command=self.show_signup,
               bg="#2196F3", fg="white", font=("Arial", 10)).pack()
    
    def show_signup(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = Frame(self.root)
        frame.pack(pady=10)
        
        # Title frame with logo3
        title_frame = Frame(frame)
        title_frame.pack(pady=5)
        
        # Load and display logo3.png with specific size using PIL
        try:
            logo3_pil = Image.open("logo3.png")
            logo3_pil = logo3_pil.resize((321, 261), Image.LANCZOS)
            logo3_img = ImageTk.PhotoImage(logo3_pil)
            logo3_label = Label(title_frame, image=logo3_img)
            logo3_label.image = logo3_img  # Keep a reference!
            logo3_label.pack(pady=(0, 5))
        except Exception as e:
            print(f"Error loading logo3.png: {e}")
        
        Label(title_frame, text="Create Account", font=("Arial", 20, "bold")).pack()
        
        # Username row
        username_frame = Frame(frame)
        username_frame.pack(pady=5)
        
        # Load and display logo.png with specific size
        try:
            logo_img = PhotoImage(file="logo.png")
            logo_img = logo_img.subsample(int(logo_img.width()/22), int(logo_img.height()/27))
            logo_label = Label(username_frame, image=logo_img)
            logo_label.image = logo_img
            logo_label.pack(side=LEFT, padx=5)
        except Exception as e:
            print(f"Error loading logo.png: {e}")
        
        # Username label and entry in same container
        username_container = Frame(username_frame)
        username_container.pack(side=LEFT)
        Label(username_container, text="Username:", font=("Arial", 10)).pack(side=LEFT, padx=(0,5))
        self.new_username = Entry(username_container, font=("Arial", 10))
        self.new_username.pack(side=LEFT)
        
        # Password row
        password_frame = Frame(frame)
        password_frame.pack(pady=5)
        
        # Load and display logo2.png with specific size
        try:
            logo2_img = PhotoImage(file="logo2.png")
            logo2_img = logo2_img.subsample(int(logo2_img.width()/22), int(logo2_img.height()/27))
            logo2_label = Label(password_frame, image=logo2_img)
            logo2_label.image = logo2_img
            logo2_label.pack(side=LEFT, padx=5)
        except Exception as e:
            print(f"Error loading logo2.png: {e}")
        
        # Password label and entry in same container
        password_container = Frame(password_frame)
        password_container.pack(side=LEFT)
        Label(password_container, text="Password:", font=("Arial", 10)).pack(side=LEFT, padx=(0,5))
        self.new_password = Entry(password_container, font=("Arial", 10), show="*")
        self.new_password.pack(side=LEFT)
        
        # Confirm Password row
        confirm_frame = Frame(frame)
        confirm_frame.pack(pady=5)
        
        # Load and display logo2.png again for confirm password
        try:
            logo2_confirm_img = PhotoImage(file="logo2.png")
            logo2_confirm_img = logo2_confirm_img.subsample(int(logo2_confirm_img.width()/22), int(logo2_confirm_img.height()/27))
            logo2_confirm_label = Label(confirm_frame, image=logo2_confirm_img)
            logo2_confirm_label.image = logo2_confirm_img
            logo2_confirm_label.pack(side=LEFT, padx=5)
        except Exception as e:
            print(f"Error loading logo2.png: {e}")
        
        # Confirm Password label and entry in same container
        confirm_container = Frame(confirm_frame)
        confirm_container.pack(side=LEFT)
        Label(confirm_container, text="Confirm Password:", font=("Arial", 10)).pack(side=LEFT, padx=(0,5))
        self.confirm_password = Entry(confirm_container, font=("Arial", 10), show="*")
        self.confirm_password.pack(side=LEFT)
        
        # Buttons with specific sizes
        Button(frame, text="Sign Up", command=self.signup,
               bg="#4CAF50", fg="white", font=("Arial", 10),
               width=15, height=1).pack(pady=10)
        
        Button(frame, text="Back to Login", command=self.show_login,
               bg="#2196F3", fg="white", font=("Arial", 10),
               width=15, height=1).pack()
    
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
        
        try:
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            
            # Check if username already exists
            c.execute("SELECT username FROM users WHERE username=?", (username,))
            if c.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return
            
            # Create new user (removed the 'role' value)
            hashed_password = hash_password(password)
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (username, hashed_password))  # Only inserting username and password
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            if 'conn' in locals():
                conn.close()
    
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