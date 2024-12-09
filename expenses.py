from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

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
	global tree
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

	# Add a vertical scrollbar for the Treeview
	scroll_y = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
	tree.config(yscrollcommand=scroll_y.set)

	# Use grid for both tree and scrollbar to align them properly
	tree.grid(row=0, column=0, sticky="nsew")
	scroll_y.grid(row=0, column=1, sticky="ns")

	# Make the tree_frame expand with the window
	tree_frame.grid_rowconfigure(0, weight=1)
	tree_frame.grid_columnconfigure(0, weight=1)

	# Fetch and display data
	refresh_treeview()

def refresh_treeview():
	# Clear existing data
	for item in tree.get_children():
		tree.delete(item)

	# Connect to the database and fetch the data
	conn = sqlite3.connect('expenses.db')
	c = conn.cursor()

	# Query the database for all expenses
	c.execute("SELECT date, category, amount, description FROM expenses")
	rows = c.fetchall()

	# Insert data into the Treeview
	for row in rows:
		tree.insert("", "end", values=row)

	# Close the database connection
	conn.close()