from tkinter import *

def setting(frame):
    """Function to set up the Expenses tab"""
    budgetlbl = Label(frame, text="Budget:", font="50")
    budgetlbl.grid(row=0, column=0, padx=50, sticky="w")

    budgetentry = Entry(frame, font="50")
    budgetentry.grid(row=0, column=1, padx=50, sticky="w")

    savebtn = Button(frame, text="Save", font="50")
    savebtn.grid(row=1, column=0, pady=10, padx=50, sticky="w")

    resetbtn = Button(frame, text="Reset All Data", font="50")
    resetbtn.grid(row=1, column=1, pady=10, padx=50, sticky="w")

    changebtn = Button(frame, text="Change Currency", font="50")
    changebtn.grid(row=2, column=0, pady=10, padx=50, sticky="w")

