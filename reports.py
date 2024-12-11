from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
import calendar

def reports(frame):
    """Function to set up the Reports tab with expense analytics"""
    # Create frames for different sections
    summary_frame = LabelFrame(frame, text="Summary", font=("Arial", 12, "bold"))
    summary_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    
    charts_frame = LabelFrame(frame, text="Expense Breakdown", font=("Arial", 12, "bold"))
    charts_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    # Summary section
    def update_summary():
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        
        # Total expenses this month
        first_day = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        last_day = datetime.now().replace(day=calendar.monthrange(datetime.now().year, datetime.now().month)[1]).strftime('%Y-%m-%d')
        c.execute("SELECT SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) FROM expenses WHERE date BETWEEN ? AND ?", (first_day, last_day))
        monthly_total = c.fetchone()[0] or 0
        
        # Total expenses this week
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
        c.execute("SELECT SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) FROM expenses WHERE date >= ?", (week_start,))
        weekly_total = c.fetchone()[0] or 0
        
        # Most expensive category
        c.execute("""
            SELECT category, SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) as total 
            FROM expenses 
            GROUP BY category 
            ORDER BY total DESC 
            LIMIT 1
        """)
        top_category = c.fetchone()
        
        # Update labels
        monthly_label.config(text=f"This Month: ₱{monthly_total:,.2f}")
        weekly_label.config(text=f"This Week: ₱{weekly_total:,.2f}")
        if top_category:
            category_label.config(text=f"Top Category: {top_category[0]} (₱{top_category[1]:,.2f})")
        
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
        
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Get total expenses
        c.execute("SELECT SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) FROM expenses")
        total_expenses = c.fetchone()[0] or 0
        
        # Get expenses by category
        c.execute("""
            SELECT category, SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) as total 
            FROM expenses 
            GROUP BY category 
            ORDER BY total DESC
        """)
        
        for category, amount in c.fetchall():
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            tree.insert("", "end", values=(category, f"₱{amount:,.2f}", f"{percentage:.1f}%"))
        
        conn.close()

    # Refresh button
    refresh_btn = Button(frame, text="Refresh Reports", command=lambda: [update_summary(), update_category_breakdown()], font=("Arial", 10))
    refresh_btn.grid(row=2, column=0, pady=10)

    # Initial update
    update_summary()
    update_category_breakdown()
