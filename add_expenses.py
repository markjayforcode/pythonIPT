from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

def add_expenses(frame):
    categories = ["Food", "Transpo", "Utilities", "Rent", "Insurance", "Health", "Education", "Entertainment", "Others"]


    """Function to set up the Expenses tab"""
    datelbl = Label(frame, text="Date:", font="50")
    datelbl.grid(row=0, column=0, padx=50, sticky="w")

    cal =  DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, font="50")
    cal.grid(row=0, column=1, padx=50, sticky="w")

    amountlbl = Label(frame, text="Amount:", font="50")
    amountlbl.grid(row=1, column=0, padx=50, sticky="w") 

    amountentry = Entry(frame, font="50")
    amountentry.grid(row=1, column=1, padx=50, sticky="w")

    categorylbl = Label(frame, text="Category:", font="50")
    categorylbl.grid(row=2, column=0, padx=50, sticky="w")

    categorymenu = ttk.Combobox(frame, values=categories, state="readonly", font="50")
    categorymenu.grid(row=2, column=1, padx=50, sticky="w")
    categorymenu.set("Select a Category")  # Default value


    descriplbl = Label(frame, text="Description:", font="50")
    descriplbl.grid(row=3, column=0, padx=50, sticky="w")

    descriptentry = Entry(frame, font="50")
    descriptentry.grid(row=3, column=1, padx=50, sticky="w")

    submitbtn = Button(frame, text="Submit", font="50")
    submitbtn.grid(row=4, column=0, pady=10, padx=50, sticky="w")


