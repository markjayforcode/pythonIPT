from tkinter import *
from tkinter import ttk
from dashboard import create_dashboard
from expenses import create_expenses
from add_expenses import add_expenses
from reports import reports
from settings import setting

def main():
    root = Tk()
    root.geometry("600x350")
    root.resizable(False, False)
    root.title("Expense Tracker")

    # Create Notebook (Tabbed Interface)
    navigationBar = ttk.Notebook(root)
    navigationBar.pack(fill="both", expand=True)

    # Dashboard Tab
    dashboard_frame = Frame(navigationBar)
    create_dashboard(dashboard_frame,navigationBar)  # Call function from dashboard.py
    navigationBar.add(dashboard_frame, text="Dashboard")

    # Expenses Tab
    addexp_frame = Frame(navigationBar)
    add_expenses(addexp_frame)  # Call function from add_expenses.py
    navigationBar.add(addexp_frame, text="Add Expenses")

    # View Expenses Tab
    expenses_frame = Frame(navigationBar)
    create_expenses(expenses_frame)  # Call function from expenses.py
    navigationBar.add(expenses_frame, text="View Expenses")

    # View Expenses Tab
    reports_frame = Frame(navigationBar)
    reports(reports_frame)  # Call function from expenses.py
    navigationBar.add(reports_frame, text="Reports")

    # Settings Tab
    setting_frame = Frame(navigationBar)
    setting(setting_frame)  # Call function from settings.py
    navigationBar.add(setting_frame, text="Settings")


   

    root.mainloop()

if __name__ == "__main__":
    main()
