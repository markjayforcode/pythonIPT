from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from database import add_expense
from expenses import refresh_treeview

def add_expenses(frame):
    categories = ["Food", "Transportation", "Utilities", "Rent", "Insurance", "Health", "Education", "Entertainment", "Others"]


    """Function to set up the Expenses tab"""
    datelbl = Label(frame, text="Date:", font="50")
    datelbl.grid(row=0, column=0, padx=50, sticky="w")

    global cal #decalred as global to access it in the submit function
    cal =  DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, font="50")
    cal.grid(row=0, column=1, padx=50, sticky="w")

    amountlbl = Label(frame, text="Amount:", font="50")
    amountlbl.grid(row=1, column=0, padx=50, sticky="w") 

    global amountentry #decalred as global to access it in the submit function
    amountentry = Entry(frame, font="50")
    amountentry.grid(row=1, column=1, padx=50, sticky="w")

    categorylbl = Label(frame, text="Category:", font="50")
    categorylbl.grid(row=2, column=0, padx=50, sticky="w")

    global categorymenu #decalred as global to access it in the submit function
    categorymenu = ttk.Combobox(frame, values=categories, state="readonly", font="50")
    categorymenu.grid(row=2, column=1, padx=50, sticky="w")
    categorymenu.set("Select a Category")  # Default value


    descriplbl = Label(frame, text="Description:", font="50")
    descriplbl.grid(row=3, column=0, padx=50, sticky="w")

    global descriptentry #decalred as global to access it in the submit function
    descriptentry = Entry(frame, font="50")
    descriptentry.grid(row=3, column=1, padx=50, sticky="w")

    submitbtn = Button(frame, text="Submit", font="50", command=submit_expense)
    submitbtn.grid(row=4, column=0, pady=10, padx=50, sticky="w")

def submit_expense():
    date = cal.get()
    amount = amountentry.get()
    category = categorymenu.get()
    description = descriptentry.get()
    
    if not amount or category == "Select a Category": 
        print("Please fill in all fields")
        return
    
    #currency symbol
    amount_with_currency = f"₱{amount}"

    add_expense(date, amount_with_currency, category, description)
    print("Expense added successfully")

    amountentry.delete(0, END)
    categorymenu.set("Select a Category")
    descriptentry.delete(0, END)

    refresh_treeview()  # Refresh the Treeview in expenses.py




