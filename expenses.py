from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from session import UserSession
from database import get_user_expenses

def create_expenses(frame):
	categories = ["Food", "Transportation", "Utilities", "Rent", "Insurance", "Health", "Education", "Entertainment", "Others"]

	# Filter section frame
	filter_frame = LabelFrame(frame, text="Filter Options", font=("Arial", 11, "bold"))
	filter_frame.grid(row=0, column=0, columnspan=7, padx=10, pady=5, sticky="ew")

	# Filter components
	filterlbl = Label(filter_frame, text="Filter by:", font=("Arial", 10))
	filterlbl.grid(row=0, column=0, padx=5, pady=5, sticky="w")

	datelbl = Label(filter_frame, text="Date:", font=("Arial", 10))
	datelbl.grid(row=0, column=1, padx=5, pady=5, sticky="w")

	datefilter = DateEntry(filter_frame, width=12, background='darkblue', 
						  foreground='white', borderwidth=2, font=("Arial", 10))
	datefilter.grid(row=0, column=2, padx=5, pady=5, sticky="w")

	categorymenu = ttk.Combobox(filter_frame, values=categories, 
							   state="readonly", font=("Arial", 10), width=15)
	categorymenu.grid(row=0, column=3, padx=5, pady=5, sticky="w")
	categorymenu.set("Category")

	def apply_filter():
		for item in tree.get_children():
			tree.delete(item)

		conn = sqlite3.connect('expenses.db')
		c = conn.cursor()
		user_id = UserSession.get_user()
		
		query = "SELECT date, category, amount, description FROM expenses WHERE user_id = ?"
		params = [user_id]

		if datefilter.get() != datetime.today().strftime('%m/%d/%y'):
			query += " AND date = ?"
			params.append(datefilter.get())
			
		if categorymenu.get() != "Category":
			query += " AND category = ?"
			params.append(categorymenu.get())

		c.execute(query, params)
		rows = c.fetchall()

		for row in rows:
			tree.insert("", "end", values=row)

		conn.close()

	def clear_filter():
		datefilter.set_date(datetime.today())
		categorymenu.set("Category")
		refresh_treeview()

	def delete_selected():
		selected_items = tree.selection()
		if not selected_items:
			messagebox.showwarning("Warning", "Please select an item to delete")
			return

		if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected expense(s)?"):
			conn = sqlite3.connect('expenses.db')
			c = conn.cursor()
			user_id = UserSession.get_user()
			
			for item in selected_items:
				values = tree.item(item)['values']
				c.execute("""DELETE FROM expenses 
						   WHERE date=? AND category=? AND amount=? AND description=? AND user_id=?""", 
						   (values[0], values[1], values[2], values[3], user_id))
			
			conn.commit()
			conn.close()
			refresh_treeview()
			messagebox.showinfo("Success", "Selected expense(s) deleted successfully")

	# Buttons frame
	button_frame = Frame(filter_frame)
	button_frame.grid(row=0, column=4, padx=5, pady=5, sticky="e")

	filterbtn = Button(button_frame, text="Apply Filter", command=apply_filter,
					  font=("Arial", 10), bg="#4CAF50", fg="white")
	filterbtn.pack(side=LEFT, padx=2)

	clearbtn = Button(button_frame, text="Clear Filter", command=clear_filter,
					 font=("Arial", 10), bg="#2196F3", fg="white")
	clearbtn.pack(side=LEFT, padx=2)

	deletebtn = Button(button_frame, text="Delete Selected", command=delete_selected,
					  font=("Arial", 10), bg="#f44336", fg="white")
	deletebtn.pack(side=LEFT, padx=2)

	# Treeview frame
	tree_frame = Frame(frame)
	tree_frame.grid(row=1, column=0, columnspan=7, pady=5, padx=10, sticky="nsew")

	# Treeview widget
	global tree
	tree = ttk.Treeview(tree_frame, columns=("Date", "Category", "Amount", "Description"), 
					   show="headings", selectmode="extended")

	# Define column headings and widths
	columns = {
		"Date": 100,
		"Category": 150,
		"Amount": 100,
		"Description": 200
	}

	for col, width in columns.items():
		tree.heading(col, text=col, command=lambda c=col: sort_treeview(c))
		tree.column(col, width=width)

	# Add scrollbars
	scroll_y = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
	scroll_x = Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
	tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

	# Grid layout for tree and scrollbars
	tree.grid(row=0, column=0, sticky="nsew")
	scroll_y.grid(row=0, column=1, sticky="ns")
	scroll_x.grid(row=1, column=0, sticky="ew")

	# Configure grid weights
	tree_frame.grid_rowconfigure(0, weight=1)
	tree_frame.grid_columnconfigure(0, weight=1)

	# Initial data load
	refresh_treeview()
	
	def auto_refresh():
		refresh_treeview()
		# Schedule next refresh in 30 seconds
		frame.after(30000, auto_refresh)
	
	# Start auto-refresh
	auto_refresh()
	
	return tree

def sort_treeview(col):
	items = [(tree.set(item, col), item) for item in tree.get_children("")]
	items.sort()
	for index, (val, item) in enumerate(items):
		tree.move(item, "", index)

def refresh_treeview():
	# Clear existing items
	for item in tree.get_children():
		tree.delete(item)
		
	try:
		# Get current user from session
		user_id = UserSession.get_user()
		if not user_id:
			messagebox.showerror("Error", "User session not found")
			return
			
		# Get expenses from database
		conn = sqlite3.connect('expenses.db')
		c = conn.cursor()
		c.execute("""
			SELECT date, category, amount, description 
			FROM expenses 
			WHERE user_id = ? 
			ORDER BY date DESC
		""", (user_id,))
		
		expenses = c.fetchall()
		
		# Insert expenses into treeview
		for expense in expenses:
			tree.insert('', 'end', values=expense)
			
		conn.close()
		
	except Exception as e:
		messagebox.showerror("Database Error", f"Failed to load expenses: {str(e)}")