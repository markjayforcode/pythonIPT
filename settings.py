from tkinter import *
from tkinter import ttk, messagebox, filedialog
from database import get_user_budget, update_user_budget
import sqlite3
import json
import os
import csv
from datetime import datetime
from session import UserSession

user_id = UserSession.get_user()  # Get the logged-in user
user_budget = get_user_budget(user_id)

# Load or create settings configuration
def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            return json.load(f)
    return {"budget": 0}

def save_settings_to_file(settings_dict):
    with open('settings.json', 'w') as f:
        json.dump(settings_dict, f)

def setting(frame):
    """Function to set up the Settings tab"""
    settings_data = load_settings()
    
    # Add Logout Frame at the top
    logout_frame = Frame(frame)
    logout_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="e")
    
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Save current settings
            try:
                budget = float(budget_var.get())
                settings_dict = {"budget": budget}
                save_settings_to_file(settings_dict)
            except ValueError:
                pass
                
            # Clear user session
            UserSession.clear()
            
            # Close main window and show login
            frame.master.master.master.destroy()
            from auth import AuthWindow
            root = Tk()
            auth_window = AuthWindow(root)
            root.mainloop()
    
    logout_btn = Button(logout_frame, text="Logout", command=logout,
                       font=("Arial", 10), bg="#f44336", fg="white")
    logout_btn.grid(row=0, column=0, padx=20)
    
    # Budget Section
    budget_frame = LabelFrame(frame, text="Budget Settings", font=("Arial", 11, "bold"))
    budget_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    budgetlbl = Label(budget_frame, text="Monthly Budget (₱):", font=("Arial", 10))
    budgetlbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")

   
   
    budget_var = StringVar(value=str(user_budget))

    budgetentry = Entry(budget_frame, font=("Arial", 10), textvariable=budget_var)
    budgetentry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Data Management Section
    data_frame = LabelFrame(frame, text="Data Management", font=("Arial", 11, "bold"))
    data_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def save_settings():
     try:
        budget = float(budget_var.get())
        if budget < 0:
            messagebox.showerror("Error", "Budget cannot be negative!")
            return
        
        user_id = UserSession.get_user()
        if update_user_budget(user_id, budget):
            messagebox.showinfo("Success", "Budget updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update budget!")
     except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for budget!")


    def reset_data():
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all data? This action cannot be undone!"):
         try:
            user_id = UserSession.get_user()
            with get_db_connection() as conn:
                c = conn.cursor()
                # Delete only this user's expenses
                c.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
                
                # Reset this user's budget
                update_user_budget(user_id, 0)
                budget_var.set("0")
                
            messagebox.showinfo("Success", "Your data has been reset successfully!")
         except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def export_data():
        user_id = UserSession.get_user()
        if not user_id:
            messagebox.showerror("Error", "Please log in first")
            return
            
        export_format = messagebox.askquestion("Export Format", 
            "Would you like to export as CSV?\n\n" +
            "Yes = CSV Format (Excel compatible)\n" +
            "No = Text Format (Plain text)")
            
        current_date = datetime.now().strftime("%Y%m%d")
        
        try:
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            
            c.execute("""
                SELECT date, category, amount, description 
                FROM expenses 
                WHERE user_id = ? 
                ORDER BY date DESC
            """, (user_id,))
            expenses = c.fetchall()
            
            if not expenses:
                messagebox.showinfo("Info", "No expenses to export")
                return
                
            if export_format == 'yes':  # CSV Format
                filename = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    initialfile=f"expenses_{current_date}.csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
                
                if filename:
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Date", "Category", "Amount", "Description"])
                        writer.writerows(expenses)
                        
                    messagebox.showinfo("Success", f"Data exported successfully to:\n{filename}")
            
            else:  # Text Format
                filename = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    initialfile=f"expenses_{current_date}.txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
                
                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("Expense Report\n")
                        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"User: {user_id}\n")
                        f.write("\n" + "="*50 + "\n\n")
                        
                        # Calculate totals using the numeric value
                        total = sum(float(amount.replace('₱', '').replace(',', '')) 
                                  for _, _, amount, _ in expenses)
                        
                        f.write(f"Total Expenses: PHP {total:,.2f}\n")  # Changed ₱ to PHP
                        f.write(f"Number of Records: {len(expenses)}\n\n")
                        f.write("-"*50 + "\n\n")
                        
                        for date, category, amount, desc in expenses:
                            f.write(f"Date: {date}\n")
                            f.write(f"Category: {category}\n")
                            f.write(f"Amount: PHP {amount.replace('₱', '')}\n")  # Changed ₱ to PHP
                            f.write(f"Description: {desc}\n")
                            f.write("-"*30 + "\n")
                            
                    messagebox.showinfo("Success", f"Data exported successfully to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
        finally:
            conn.close()

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

