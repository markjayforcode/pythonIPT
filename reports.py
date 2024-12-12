from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
import calendar
from session import UserSession

def reports(frame):
    """Function to set up the Reports tab with expense analytics"""
    # Create frames for different sections
    summary_frame = LabelFrame(frame, text="Summary", font=("Arial", 12, "bold"))
    summary_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    
    charts_frame = LabelFrame(frame, text="Expense Breakdown", font=("Arial", 12, "bold"))
    charts_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    def update_summary():
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        user_id = UserSession.get_user()
        
        # Total expenses this month
        first_day = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        last_day = datetime.now().replace(day=calendar.monthrange(datetime.now().year, datetime.now().month)[1]).strftime('%Y-%m-%d')
        c.execute("""
            SELECT SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) 
            FROM expenses 
            WHERE date BETWEEN ? AND ? AND user_id = ?
        """, (first_day, last_day, user_id))
        monthly_total = c.fetchone()[0] or 0
        
        # Total expenses this week
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
        c.execute("""
            SELECT SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) 
            FROM expenses 
            WHERE date >= ? AND user_id = ?
        """, (week_start, user_id))
        weekly_total = c.fetchone()[0] or 0
        
        # Most expensive category
        c.execute("""
            SELECT category, SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) as total 
            FROM expenses 
            WHERE user_id = ?
            GROUP BY category 
            ORDER BY total DESC 
            LIMIT 1
        """, (user_id,))
        top_category = c.fetchone()
        
        # Update labels
        monthly_label.config(text=f"This Month: ₱{monthly_total:,.2f}")
        weekly_label.config(text=f"This Week: ₱{weekly_total:,.2f}")
        if top_category:
            category_label.config(text=f"Top Category: {top_category[0]} (₱{top_category[1]:,.2f})")
        else:
            category_label.config(text="No expenses recorded yet")
        
        conn.close()

    monthly_label = Label(summary_frame, text="This Month: ₱0.00", font=("Arial", 11))
    monthly_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    
    weekly_label = Label(summary_frame, text="This Week: ₱0.00", font=("Arial", 11))
    weekly_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    
    category_label = Label(summary_frame, text="Top Category: None", font=("Arial", 11))
    category_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    # Category breakdown section
    tree = ttk.Treeview(charts_frame, columns=("Category", "Total", "Percentage"), show="headings", height=8)
    tree.heading("Category", text="Category")
    tree.heading("Total", text="Total Amount")
    tree.heading("Percentage", text="% of Expenses")
    
    tree.column("Category", width=150)
    tree.column("Total", width=150)
    tree.column("Percentage", width=150)
    
    tree.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    def update_category_breakdown():
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        user_id = UserSession.get_user()
        
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Get total expenses for current user
        c.execute("""
            SELECT SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) 
            FROM expenses 
            WHERE user_id = ?
        """, (user_id,))
        total_expenses = c.fetchone()[0] or 0
        
        # Get expenses by category for current user
        c.execute("""
            SELECT category, SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) as total 
            FROM expenses 
            WHERE user_id = ?
            GROUP BY category 
            ORDER BY total DESC
        """, (user_id,))
        
        for category, amount in c.fetchall():
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            tree.insert("", "end", values=(category, f"₱{amount:,.2f}", f"{percentage:.1f}%"))
        
        conn.close()

    # Refresh button with improved visibility
    refresh_btn = Button(frame, text="↻ Refresh Reports", command=lambda: [update_summary(), update_category_breakdown()],
                        font=("Arial", 10, "bold"), bg="#2196F3", fg="white", padx=20)
    refresh_btn.grid(row=2, column=0, pady=10)

    # Initial update
    update_summary()
    update_category_breakdown()

    # Configure grid weights
    frame.grid_columnconfigure(0, weight=1)

def get_category_totals():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    user_id = UserSession.get_user()
    
    c.execute("""
        SELECT category, SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,))
    
    totals = c.fetchall()
    conn.close()
    return totals
