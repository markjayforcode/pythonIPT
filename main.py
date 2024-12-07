from tkinter import *

root = Tk() 
root.geometry("600x350")
root.resizable(height=False, width=False)
root.title("Expense Tracker")

# Total Expense and Total Budget Labels with minimal column gap
totExp = Label(root, text="Total Expense: N/A", font="50") 
totExp.grid(row=0, column=0, padx=(80,0), sticky="w")  # Left-aligned with some padding

totBud = Label(root, text="Total Budget: N/A", font="50")
totBud.grid(row=0, column=1, padx=(50,50), sticky="w")  # Close to the first label

addExp = Button(root, text="Add Expense", font="50")
addExp.grid(row=1, column=0, padx=(80,0), pady=(20,0), sticky="w")  # Left-aligned with some padding

viewExp = Button(root, text="View Expenses", font="50")
viewExp.grid(row=1, column=1, padx=(50,50), pady=(20,0), sticky="w")  # Close to the first button

root.mainloop()
