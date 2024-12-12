from tkinter import *
from tkinter import ttk
import sqlite3
from settings import load_settings
from session import UserSession

def create_dashboard(frame, navigationBar):
    """Function to set up the Dashboard tab"""
    # Main title
    title_label = Label(frame, text="Expense Tracker Dashboard", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

    # Create summary frame
    summary_frame = LabelFrame(frame, text="Overview", font=("Arial", 12, "bold"), padx=20, pady=10)
    summary_frame.grid(row=1, column=0, columnspan=2, padx=20, sticky="ew")

    def update_dashboard():
        # Get budget from settings
        settings = load_settings()
        budget = settings.get("budget", 0)
        
        # Get total expenses for current user
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        user_id = UserSession.get_user()
        c.execute("""
            SELECT SUM(CAST(REPLACE(REPLACE(amount, '₱', ''), ',', '') AS DECIMAL)) 
            FROM expenses 
            WHERE user_id = ?
        """, (user_id,))
        total = c.fetchone()[0] or 0
        conn.close()
        
        # Update labels
        totExp.config(text=f"₱{total:,.2f}")
        totBud.config(text=f"₱{budget:,.2f}")
        
        # Update remaining budget
        remaining = budget - total
        remaining_label.config(text=f"₱{remaining:,.2f}")
        
        # Update status
        if remaining < 0:
            status_label.config(text="OVER BUDGET!", fg="red")
        elif remaining == 0:
            status_label.config(text="ON BUDGET", fg="orange")
        else:
            status_label.config(text="UNDER BUDGET", fg="green")

    # Budget Information
    Label(summary_frame, text="Total Budget:", font=("Arial", 11)).grid(row=0, column=0, pady=5, sticky="w")
    totBud = Label(summary_frame, text="₱0.00", font=("Arial", 11, "bold"))
    totBud.grid(row=0, column=1, pady=5, sticky="w")

    Label(summary_frame, text="Total Expenses:", font=("Arial", 11)).grid(row=1, column=0, pady=5, sticky="w")
    totExp = Label(summary_frame, text="₱0.00", font=("Arial", 11, "bold"))
    totExp.grid(row=1, column=1, pady=5, sticky="w")

    Label(summary_frame, text="Remaining Budget:", font=("Arial", 11)).grid(row=2, column=0, pady=5, sticky="w")
    remaining_label = Label(summary_frame, text="₱0.00", font=("Arial", 11, "bold"))
    remaining_label.grid(row=2, column=1, pady=5, sticky="w")

    Label(summary_frame, text="Status:", font=("Arial", 11)).grid(row=3, column=0, pady=5, sticky="w")
    status_label = Label(summary_frame, text="N/A", font=("Arial", 11, "bold"))
    status_label.grid(row=3, column=1, pady=5, sticky="w")

    # Quick Actions Frame
    actions_frame = LabelFrame(frame, text="Quick Actions", font=("Arial", 12, "bold"), padx=20, pady=10)
    actions_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    addExp = Button(actions_frame, text="Add New Expense", font=("Arial", 10),
                   command=lambda: navigationBar.select(1),
                   bg="#4CAF50", fg="white", width=20, pady=5)
    addExp.grid(row=0, column=0, pady=10, padx=10)

    viewExp = Button(actions_frame, text="View All Expenses", font=("Arial", 10),
                    command=lambda: navigationBar.select(2),
                    bg="#2196F3", fg="white", width=20, pady=5)
    viewExp.grid(row=0, column=1, pady=10, padx=10)

    # Refresh button
    refresh_btn = Button(frame, text="Refresh Dashboard", command=update_dashboard,
                        font=("Arial", 10), bg="#9C27B0", fg="white")
    refresh_btn.grid(row=3, column=0, columnspan=2, pady=10)

    # Initial update
    update_dashboard()
