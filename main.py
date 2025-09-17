import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from openpyxl import Workbook
from tkinter import filedialog
from tkcalendar import DateEntry  # New import for date picker
from analyze_expenses import analyze_expenses  # Import the analysis function
import  analyze_expenses_002
from tkinter import ttk # New import for Treeview
from config import DATABASE_NAME # Import DATABASE_NAME
import logging # Import logging

# Configure logging
logging.basicConfig(filename='budget_app.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Create and connect to SQLite database
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    amount REAL,
                    date TEXT)''')
conn.commit()

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Budget Calculator")
        self.root.geometry("700x700") # Adjusted window size

        # Variables
        self.total_spent = tk.DoubleVar()
        self.amount = tk.DoubleVar()

        # Create UI components
        self.create_widgets()

        # Update total spent and recent expenses initially
        self.update_total_spent()
        self.display_recent_expenses()

    def create_widgets(self):
        # Configure grid weights for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Styling
        label_font = ("Arial", 11)
        button_font = ("Arial", 10, "bold")
        header_font = ("Arial", 16, "bold")
        total_label_font = ("Arial", 18, "bold")

        # --- Input Section ---
        input_frame = tk.LabelFrame(self.root, text="Add New Expense", font=header_font, padx=10, pady=10)
        input_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        tk.Label(input_frame, text="Description:", font=label_font).grid(row=0, column=0, pady=5, sticky="w")
        self.description_text = tk.Text(input_frame, height=2, width=35)
        self.description_text.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        tk.Label(input_frame, text="Amount:", font=label_font).grid(row=2, column=0, pady=5, sticky="w")
        self.amount_entry = tk.Entry(input_frame, textvariable=self.amount, width=35)
        self.amount_entry.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        tk.Label(input_frame, text="Select Date:", font=label_font).grid(row=4, column=0, pady=5, sticky="w")
        self.date_entry = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

        add_button = tk.Button(input_frame, text="Add Expense", command=self.add_expense, font=button_font, bg="#4CAF50", fg="white")
        add_button.grid(row=6, column=0, columnspan=2, pady=10)

        # --- Expense List Section ---
        list_frame = tk.LabelFrame(self.root, text="Recent Expenses", font=header_font, padx=10, pady=10)
        list_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.root.grid_rowconfigure(1, weight=1) # Make this row expandable

        self.expense_tree = ttk.Treeview(list_frame, columns=("ID", "Description", "Amount", "Date"), show="headings")
        self.expense_tree.heading("ID", text="ID")
        self.expense_tree.heading("Description", text="Description")
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.heading("Date", text="Date")

        self.expense_tree.column("ID", width=50, anchor="center")
        self.expense_tree.column("Description", width=200, anchor="w")
        self.expense_tree.column("Amount", width=100, anchor="e")
        self.expense_tree.column("Date", width=150, anchor="center")

        self.expense_tree.pack(fill="both", expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.expense_tree.yview)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # --- Summary and Actions Section ---
        summary_frame = tk.Frame(self.root)
        summary_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.total_label = tk.Label(summary_frame, text="Total Spent: $0.00", font=total_label_font, fg="#3F51B5")
        self.total_label.pack(pady=10)

        self.breakdown_label = tk.Label(summary_frame, text="", font=("Arial", 12), justify="left")
        self.breakdown_label.pack(pady=10)

        action_buttons_frame = tk.Frame(self.root)
        action_buttons_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        calculate_button = tk.Button(action_buttons_frame, text="Calculate Daily Total", command=self.calculate_total, font=button_font, bg="#2196F3", fg="white")
        calculate_button.pack(side=tk.LEFT, padx=5)

        analyze_button = tk.Button(action_buttons_frame, text="Analyze Expenses (Chart)", command=analyze_expenses, font=button_font, bg="#FFC107", fg="black")
        analyze_button.pack(side=tk.LEFT, padx=5)

        export_button = tk.Button(action_buttons_frame, text="Export to Excel", command=analyze_expenses_002.export_to_excel, font=button_font, bg="#607D8B", fg="white")
        export_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(action_buttons_frame, text="Clear All Data", command=self.clear_database, bg='red', fg='white', font=button_font)
        clear_button.pack(side=tk.LEFT, padx=5)

    def add_expense(self):
        description = self.description_text.get("1.0", "end-1c")
        amount_str = self.amount_entry.get() # Get string from entry
        
        try:
            amount = float(amount_str) # Ensure amount is a float
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for amount.")
            return

        # Use the date from the DateEntry widget
        selected_date = self.date_entry.get_date().strftime("%Y-%m-%d %H:%M:%S")

        if not description or amount <= 0:
            messagebox.showerror("Error", "Please enter a valid description and a positive amount.")
            return

        # Insert into database
        try:
            cursor.execute("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)", (description, amount, selected_date))
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully!") # User feedback

            # Clear the inputs
            self.description_text.delete("1.0", tk.END)
            self.amount_entry.delete(0, tk.END)
            self.amount.set(0.0) # Reset the DoubleVar
            self.date_entry.set_date(datetime.now()) # Reset date to current

            # Update the total spent and recent expenses
            self.update_total_spent()
            self.display_recent_expenses()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            conn.rollback() # Rollback changes if an error occurs

    def update_total_spent(self):
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0]
        if total is None:
            total = 0.0
        self.total_spent.set(total)
        self.total_label.config(text=f"Total Spent: ${total:.2f}")

    def display_recent_expenses(self):
        # Clear existing entries in the Treeview
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)

        # Fetch recent expenses (e.g., last 10)
        cursor.execute("SELECT id, description, amount, date FROM expenses ORDER BY date DESC LIMIT 10")
        recent_data = cursor.fetchall()

        # Insert data into the Treeview
        for row in recent_data:
            self.expense_tree.insert("", "end", values=row)

    def calculate_total(self):
        selected_date = self.date_entry.get_date().strftime('%Y-%m-%d')  # Get the selected date from DateEntry

        # Query to get the expense breakdown for the selected date
        cursor.execute('''SELECT description, SUM(amount) 
                          FROM expenses 
                          WHERE DATE(date) = ? 
                          GROUP BY description''', (selected_date,))
        data = cursor.fetchall()

        if not data:
            self.breakdown_label.config(text=f"No expenses found for {selected_date}")
            return

        # Format and display the expense breakdown in breakdown_label
        breakdown_text = f"Expenses on {selected_date}:\n\n"
        total = 0.0
        for description, amount in data:
            breakdown_text += f"{description}: ${amount:.2f}\n"
            total += amount

        breakdown_text += f"\nDaily Total: ${total:.2f}"
        self.breakdown_label.config(text=breakdown_text)
        messagebox.showinfo("Daily Expense Summary", f"Total spent on {selected_date}: ${total:.2f}\n\n{breakdown_text}")

    def clear_database(self):
        response = messagebox.askyesno("Clear Database", "Are you sure you want to clear ALL expense data?")
        if response:
            try:
                cursor.execute("DELETE FROM expenses")
                conn.commit()
                self.update_total_spent()
                self.display_recent_expenses() # Clear recent expenses display
                self.breakdown_label.config(text="")  # Clear breakdown
                messagebox.showinfo("Success", "Database cleared successfully!")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred while clearing data: {e}")
                conn.rollback()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
