from tkinter import *
from tkinter import ttk
from dashboard import create_dashboard
from expenses import create_expenses
from add_expenses import add_expenses
from reports import reports
from settings import setting
from auth import AuthWindow
from database import create_tables
from migrate_database import migrate_database
from session import UserSession
import os
import sqlite3

def initialize_main_window(root):
    # Verify user session before creating main window
    if not UserSession.is_valid():
        root.destroy()
        return
        
    root.geometry("800x600")
    root.resizable(True, True)
    root.title(f"Expense Tracker - {UserSession.get_user()}")

    # Create main container
    main_container = Frame(root)
    main_container.pack(fill="both", expand=True)

    # Create Notebook (Tabbed Interface)
    navigationBar = ttk.Notebook(main_container)
    navigationBar.pack(fill="both", expand=True)

    # Add tabs with auto-refresh functionality
    dashboard_frame = Frame(navigationBar)
    create_dashboard(dashboard_frame, navigationBar)
    navigationBar.add(dashboard_frame, text="Dashboard")

    addexp_frame = Frame(navigationBar)
    add_expenses(addexp_frame)
    navigationBar.add(addexp_frame, text="Add Expenses")

    expenses_frame = Frame(navigationBar)
    create_expenses(expenses_frame)
    navigationBar.add(expenses_frame, text="View Expenses")

    reports_frame = Frame(navigationBar)
    reports(reports_frame)
    navigationBar.add(reports_frame, text="Reports")

    setting_frame = Frame(navigationBar)
    setting(setting_frame)
    navigationBar.add(setting_frame, text="Settings")

    # Add periodic refresh for all tabs
    def refresh_all():
        current_tab = navigationBar.select()
        if current_tab:
            tab_name = navigationBar.tab(current_tab, "text")
            if tab_name == "Dashboard":
                dashboard_frame.event_generate("<<Refresh>>")
            elif tab_name == "View Expenses":
                expenses_frame.event_generate("<<Refresh>>")
            elif tab_name == "Reports":
                reports_frame.event_generate("<<Refresh>>")
        root.after(5000, refresh_all)  # Refresh every 5 seconds

    refresh_all()

def main():
    # Ensure database exists and is properly initialized
    if not os.path.exists('expenses.db'):
        create_tables()
    else:
        # Verify database integrity
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM sqlite_master WHERE type='table'")
            tables = c.fetchall()
            if not any(table[1] == 'expenses' for table in tables):
                create_tables()
        finally:
            conn.close()
    
    # Start with login window
    login_root = Tk()
    auth_window = AuthWindow(login_root)
    login_root.mainloop()

if __name__ == "__main__":
    main()
