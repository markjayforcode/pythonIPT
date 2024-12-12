from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import add_expense
from expenses import refresh_treeview
from settings import load_settings
from datetime import datetime
from session import UserSession
import sqlite3

def get_monthly_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    
    current_date = datetime.now()
    first_day = current_date.replace(day=1).strftime('%Y-%m-%d')
    last_day = current_date.replace(day=1).strftime('%Y-%m-%d')
    
    user_id = UserSession.get_user()
    c.execute("""
        SELECT SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) 
        FROM expenses 
        WHERE date BETWEEN ? AND ? AND user_id = ?
    """, (first_day, last_day, user_id))
    
    total = c.fetchone()[0] or 0
    conn.close()
    return total

def add_expenses(frame):
    categories = ["Food", "Transportation", "Utilities", "Rent", "Insurance", 
                 "Health", "Education", "Entertainment", "Others"]

    # Title
    title_label = Label(frame, text="Add New Expense", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

    # Create main input frame
    input_frame = LabelFrame(frame, text="Expense Details", font=("Arial", 11, "bold"))
    input_frame.grid(row=1, column=0, columnspan=2, padx=20, sticky="ew")

    # Date input
    datelbl = Label(input_frame, text="Date:", font=("Arial", 10))
    datelbl.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    global cal
    cal = DateEntry(input_frame, width=20, background='darkblue', 
                   foreground='white', borderwidth=2, font=("Arial", 10))
    cal.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Amount input
    amountlbl = Label(input_frame, text="Amount (₱):", font=("Arial", 10))
    amountlbl.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    global amountentry
    amountentry = Entry(input_frame, font=("Arial", 10), width=22)
    amountentry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Category input
    categorylbl = Label(input_frame, text="Category:", font=("Arial", 10))
    categorylbl.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    global categorymenu
    categorymenu = ttk.Combobox(input_frame, values=categories, 
                               state="readonly", font=("Arial", 10), width=19)
    categorymenu.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    categorymenu.set("Select a Category")

    # Description input
    descriplbl = Label(input_frame, text="Description:", font=("Arial", 10))
    descriplbl.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    global descriptentry
    descriptentry = Entry(input_frame, font=("Arial", 10), width=22)
    descriptentry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    def submit_expense():
        date = cal.get()
        amount = amountentry.get()
        category = categorymenu.get()
        description = descriptentry.get()
        
        if not amount or category == "Select a Category": 
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            amount_value = float(amount.replace('₱', '').replace(',', ''))
            
            # Get monthly budget from settings
            settings = load_settings()
            monthly_budget = float(settings.get('budget', 0))
            
            # Get current monthly expenses
            current_monthly_expenses = get_monthly_expenses()
            
            # Check if this expense would exceed the budget
            if monthly_budget > 0 and (current_monthly_expenses + amount_value) > monthly_budget:
                exceed_amount = current_monthly_expenses + amount_value - monthly_budget
                warning = messagebox.askyesno(
                    "Budget Warning",
                    f"⚠️ Budget Warning!\n\nThis expense will exceed your monthly budget by ₱{exceed_amount:,.2f}!\n\nDo you want to proceed?"
                )
                if not warning:
                    return
            
            amount_with_currency = f"₱{amount_value:,.2f}"
            user_id = UserSession.get_user()
            
            if not user_id:
                messagebox.showerror("Error", "User session not found. Please log in again.")
                return
                
            add_expense(date, amount_with_currency, category, description, user_id)
            messagebox.showinfo("Success", "Expense added successfully")
            
            # Clear fields
            amountentry.delete(0, END)
            categorymenu.set("Select a Category")
            descriptentry.delete(0, END)
            
            # Refresh the expenses view
            refresh_treeview()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    # Submit button
    submitbtn = Button(frame, text="Add Expense", font=("Arial", 10), 
                      command=submit_expense, bg="#4CAF50", fg="white", width=20)
    submitbtn.grid(row=2, column=0, columnspan=2, pady=20)

    # Configure grid weights
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)




