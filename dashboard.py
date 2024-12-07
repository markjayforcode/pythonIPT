from tkinter import *

def create_dashboard(frame,navigationBar):
    """Function to set up the Dashboard tab"""
    totExp = Label(frame, text="Total Expense: N/A", font="50")
    totExp.grid(row=1, column=0, padx=50 ,sticky="w")

    totBud = Label(frame, text="Total Budget: N/A", font="50")
    totBud.grid(row=1, column=1, padx=50, sticky="w") 

    """Function to set up the Expenses tab"""
    addExp = Button(frame, text="Add Expense", font="50",command=lambda: navigationBar.select(2),)
    addExp.grid(row=2, column=0, pady=30,padx=50, sticky="w")

    viewExp = Button(frame, text="View Expenses", font="50")
    viewExp.grid(row=2, column=1, pady=30,padx=50,sticky="w")
