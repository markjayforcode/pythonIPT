from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

def create_expenses(frame):

    categories = ["Food", "Transportation", "Utilities", "Rent", "Insurance", "Health", "Education", "Entertainment", "Others"]

    # Filter section (date and category filters)
    filterlbl = Label(frame, text="Filter by:", font="20")
    filterlbl.grid(row=0, column=0, sticky="w")

    datelbl = Label(frame, text="Date:", font="20")
    datelbl.grid(row=0, column=1, padx=(10, 0), sticky="w")

    datefilter = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, font="20")
    datefilter.grid(row=0, column=2, padx=(10, 0), sticky="w")

    categorymenu = ttk.Combobox(frame, values=categories, state="readonly", font="20", width=15)
    categorymenu.grid(row=0, column=5, padx=(10, 0), sticky="w")
    categorymenu.set("Category")  # Default value

    filterbtn = Button(frame, text="Filter", font="50")
    filterbtn.grid(row=0, column=6, padx=(10, 0), sticky="w")

    # New frame for Treeview table
    tree_frame = Frame(frame)  # Create a new frame for the Treeview
    tree_frame.grid(row=1, column=0, columnspan=7, pady=10, padx=10, sticky="nsew")  # Place it in grid

    # Treeview widget for expenses
    tree = ttk.Treeview(tree_frame, columns=("Date", "Category", "Amount", "Description"), show="headings")

    # Define column headings
    tree.heading("Date", text="Date")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    tree.heading("Description", text="Description")

    # Define column widths (optional)
    tree.column("Date", width=100)
    tree.column("Category", width=150)
    tree.column("Amount", width=100)
    tree.column("Description", width=200)

    # Insert example data
    tree.insert("", "end", values=("2024-12-09", "Food", "$25", "Lunch"))
    tree.insert("", "end", values=("2024-12-08", "Transportation", "$15", "Bus fare"))

    # Add a vertical scrollbar for the Treeview
    scroll_y = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.config(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    # Add the Treeview to the frame
    tree.pack(fill="both", expand=True)
