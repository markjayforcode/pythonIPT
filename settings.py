from tkinter import *

def setting(frame):
    """Function to set up the Expenses tab"""
    lbl1 = Label(frame, text="Monthly Budget:", font="50")
    lbl1.grid(row=0, column=0, padx=50, sticky="w")

    inpBud = Entry(frame, font="50")
    inpBud.grid(row=0, column=1, padx=50, sticky="w")
    
    saveButton = Button(frame, text="Save", font="50")
    saveButton.grid(row=1, column=0, pady=10, padx=50, sticky="w")
    
