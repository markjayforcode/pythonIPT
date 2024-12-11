from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import json
import os

# Load or create settings configuration
def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            return json.load(f)
    return {"budget": 0, "currency": "₱"}

def save_settings_to_file(settings_dict):
    with open('settings.json', 'w') as f:
        json.dump(settings_dict, f)

def setting(frame):
    """Function to set up the Settings tab"""
    settings_data = load_settings()
    
    # Budget Section
    budget_frame = LabelFrame(frame, text="Budget Settings", font=("Arial", 11, "bold"))
    budget_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    budgetlbl = Label(budget_frame, text="Monthly Budget:", font=("Arial", 10))
    budgetlbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    budget_var = StringVar(value=str(settings_data.get("budget", 0)))
    budgetentry = Entry(budget_frame, font=("Arial", 10), textvariable=budget_var)
    budgetentry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Currency Section
    currency_frame = LabelFrame(frame, text="Currency Settings", font=("Arial", 11, "bold"))
    currency_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    currencylbl = Label(currency_frame, text="Select Currency:", font=("Arial", 10))
    currencylbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    currencies = ["₱", "$", "€", "£", "¥"]
    currency_var = StringVar(value=settings_data.get("currency", "₱"))
    currency_menu = ttk.Combobox(currency_frame, values=currencies, 
                                textvariable=currency_var, state="readonly", 
                                font=("Arial", 10), width=10)
    currency_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Data Management Section
    data_frame = LabelFrame(frame, text="Data Management", font=("Arial", 11, "bold"))
    data_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def save_settings():
        try:
            budget = float(budget_var.get())
            if budget < 0:
                messagebox.showerror("Error", "Budget cannot be negative!")
                return
                
            settings_dict = {
                "budget": budget,
                "currency": currency_var.get()
            }
            save_settings_to_file(settings_dict)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for budget!")

    def reset_data():
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all data? This action cannot be undone!"):
            try:
                conn = sqlite3.connect('expenses.db')
                c = conn.cursor()
                c.execute("DELETE FROM expenses")
                conn.commit()
                conn.close()
                
                # Reset settings to default
                settings_dict = {"budget": 0, "currency": "₱"}
                save_settings_to_file(settings_dict)
                budget_var.set("0")
                currency_var.set("₱")
                
                messagebox.showinfo("Success", "All data has been reset successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def export_data():
        try:
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            c.execute("SELECT * FROM expenses")
            rows = c.fetchall()
            
            with open('expenses_export.csv', 'w') as f:
                f.write("Date,Amount,Category,Description\n")
                for row in rows:
                    f.write(f"{row[1]},{row[2]},{row[3]},{row[4]}\n")
            
            messagebox.showinfo("Success", "Data exported to 'expenses_export.csv'")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

    # Buttons
    savebtn = Button(data_frame, text="Save Settings", command=save_settings,
                     font=("Arial", 10), bg="#4CAF50", fg="white")
    savebtn.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    resetbtn = Button(data_frame, text="Reset All Data", command=reset_data,
                      font=("Arial", 10), bg="#f44336", fg="white")
    resetbtn.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    exportbtn = Button(data_frame, text="Export Data", command=export_data,
                       font=("Arial", 10), bg="#2196F3", fg="white")
    exportbtn.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    # Configure grid weights
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

