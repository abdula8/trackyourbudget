import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from openpyxl import Workbook
from tkinter import filedialog
from tkcalendar import DateEntry  # New import for date picker
from analyze_expenses import analyze_expenses  # Import the analysis function

# Create and connect to SQLite database
conn = sqlite3.connect('budget.db')
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
        self.root.geometry("500x600")

        # Variables
        self.total_spent = tk.DoubleVar()
        self.amount = tk.DoubleVar()

        # Create UI components
        self.create_widgets()

        # Update total spent initially
        self.update_total_spent()

    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="Description").pack(pady=5)
        self.description_text = tk.Text(self.root, height=2, width=40)
        self.description_text.pack(pady=5)

        tk.Label(self.root, text="Amount").pack(pady=5)
        self.amount_entry = tk.Entry(self.root, textvariable=self.amount)
        self.amount_entry.pack(pady=5)

        # Buttons
        add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        add_button.pack(pady=5)

        # Date Entry for selecting a specific date
        tk.Label(self.root, text="Select a Date").pack(pady=5)
        self.date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        calculate_button = tk.Button(self.root, text="Calculate Total", command=self.calculate_total)
        calculate_button.pack(pady=5)

        analyze_button = tk.Button(self.root, text="Analyze Expenses", command=analyze_expenses)
        analyze_button.pack(pady=20)

        clear_button = tk.Button(self.root, text="Clear Database", command=self.clear_database, bg='red', fg='white')
        clear_button.pack(pady=5)
        clear_button.place(x=15, y=460)

        export_button = tk.Button(self.root, text="Export to Excel", command=self.export_to_excel)
        export_button.pack(pady=5)

        # Total spent display
        self.total_label = tk.Label(self.root, text="Total Spent: $0.00", font=("Arial", 12))
        self.total_label.pack(pady=20)

        # Expense breakdown display
        self.breakdown_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left")
        self.breakdown_label.pack(pady=10)

    def add_expense(self):
        description = self.description_text.get("1.0", "end-1c")
        amount = self.amount.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Store date and time directly

        if not description or amount <= 0:
            messagebox.showerror("Error", "Please enter a valid description and amount")
            return

        # Insert into database
        cursor.execute("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)", (description, amount, date))
        conn.commit()

        # Clear the inputs
        self.description_text.delete("1.0", tk.END)
        self.amount_entry.delete(0, tk.END)

        # Update the total spent
        self.update_total_spent()

    def update_total_spent(self):
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0]
        if total is None:
            total = 0.0
        self.total_spent.set(total)
        self.total_label.config(text=f"Total Spent: ${total:.2f}")

    def calculate_total(self):
        selected_date = self.date_entry.get_date().strftime('%Y-%m-%d')  # Get the selected date from DateEntry

        # Query to get the expense breakdown for the selected date
        cursor.execute('''SELECT description, SUM(amount) 
                          FROM expenses 
                          WHERE DATE(date) = ? 
                          GROUP BY description''', (selected_date,))
        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", f"No expenses found for {selected_date}")
            self.breakdown_label.config(text="")
            return

        # Format and display the expense breakdown
        breakdown_text = f"Expenses on {selected_date}:\n\n"
        total = 0.0
        for description, amount in data:
            breakdown_text += f"{description}: ${amount:.2f}\n"
            total += amount

        # Show the total spent at the end
        breakdown_text += f"\nTotal Spent: ${total:.2f}"

        # self.breakdown_label.config(text=breakdown_text)
        messagebox.showinfo("Total Expense", f"Total spent: ${breakdown_text}\n${total:.2f}")

    def clear_database(self):
        response = messagebox.askyesno("Clear Database", "Are you sure you want to clear all data?")
        if response:
            cursor.execute("DELETE FROM expenses")
            conn.commit()
            self.update_total_spent()
            self.breakdown_label.config(text="")  # Clear breakdown
            messagebox.showinfo("Success", "Database cleared successfully!")

    def export_to_excel(self):
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()

        if not data:
            messagebox.showerror("Error", "No data to export!")
            return

        # Create a new Excel workbook and add data
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Expenses"

        # Add headers
        headers = ['ID', 'Description', 'Amount', 'Date']
        sheet.append(headers)

        # Add data rows
        for row in data:
            sheet.append(row)

        # Save Excel file
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            workbook.save(file_path)
            messagebox.showinfo("Success", f"Data exported successfully to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
