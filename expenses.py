from tkinter import *

def create_expenses(frame):
    """Function to set up the Expenses tab"""
    addExp = Button(frame, text="Add Expense", font="50")
    addExp.pack(pady=10)

    viewExp = Button(frame, text="View Expenses", font="50")
    viewExp.pack(pady=10)
