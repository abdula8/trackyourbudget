import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from datetime import datetime
from openpyxl import Workbook
from tkcalendar import DateEntry

# Create and connect to SQLite database
conn = sqlite3.connect('budget.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    amount REAL,
                    date TEXT)''')
conn.commit()

# Define category keywords
CATEGORY_KEYWORDS = {
    "Food": ["restaurant", "lunch", "dinner", "breakfast", "snack", "coffee"],
    "Transport": ["taxi", "bus", "fuel", "gas", "metro"],
    "Entertainment": ["movie", "cinema", "concert", "game"],
    "Bills": ["electricity", "water", "internet", "phone", "rent"],
    "Shopping": ["clothes", "shoes", "grocery", "supermarket"],
    "Other": []
}

def categorize_expense(description):
    description_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in description_lower for keyword in keywords):
            return category
    return "Other"

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Budget Calculator")
        self.root.geometry("500x700")
        self.root.configure(bg="#f4f4f4")

        # Variables
        self.total_spent = tk.DoubleVar()
        self.amount = tk.DoubleVar()

        # Create UI components
        self.create_widgets()
        self.update_total_spent()

    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="Description", bg="#f4f4f4", font=("Arial", 12)).pack(pady=5)
        self.description_text = tk.Text(self.root, height=2, width=40)
        self.description_text.pack(pady=5)

        tk.Label(self.root, text="Amount", bg="#f4f4f4", font=("Arial", 12)).pack(pady=5)
        self.amount_entry = tk.Entry(self.root, textvariable=self.amount)
        self.amount_entry.pack(pady=5)

        # Buttons with colors
        add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense, bg="#4CAF50", fg="white", width=20)
        add_button.pack(pady=5)

        tk.Label(self.root, text="Select a Date", bg="#f4f4f4", font=("Arial", 12)).pack(pady=5)
        self.date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        calculate_button = tk.Button(self.root, text="Calculate Total", command=self.calculate_total, bg="#008CBA", fg="white", width=20)
        calculate_button.pack(pady=5)

        analyze_button = tk.Button(self.root, text="Analyze Expenses", command=self.analyze_expenses, bg="#f39c12", fg="white", width=20)
        analyze_button.pack(pady=5)

        clear_button = tk.Button(self.root, text="Clear Database", command=self.clear_database, bg='red', fg='white', width=20)
        clear_button.pack(pady=5)

        export_button = tk.Button(self.root, text="Export to Excel", command=self.export_to_excel, bg="#9b59b6", fg="white", width=20)
        export_button.pack(pady=5)

        # Total spent display
        self.total_label = tk.Label(self.root, text="Total Spent: $0.00", font=("Arial", 14, "bold"), bg="#f4f4f4")
        self.total_label.pack(pady=10)

    def add_expense(self):
        description = self.description_text.get("1.0", "end-1c").strip()
        amount = self.amount.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not description or amount <= 0:
            messagebox.showerror("Error", "Please enter a valid description and amount")
            return

        cursor.execute("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)", (description, amount, date))
        conn.commit()

        self.description_text.delete("1.0", tk.END)
        self.amount_entry.delete(0, tk.END)
        self.update_total_spent()

    def update_total_spent(self):
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0.0
        self.total_label.config(text=f"Total Spent: ${total:.2f}")

    def calculate_total(self):
        selected_date = self.date_entry.get_date().strftime('%Y-%m-%d')
        cursor.execute("SELECT description, SUM(amount) FROM expenses WHERE DATE(date) = ? GROUP BY description", (selected_date,))
        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", f"No expenses found for {selected_date}")
            return

        breakdown_text = f"Expenses on {selected_date}:\n\n"
        total = 0.0
        for description, amount in data:
            breakdown_text += f"{description}: ${amount:.2f}\n"
            total += amount
        breakdown_text += f"\nTotal Spent: ${total:.2f}"
        messagebox.showinfo("Total Expense", breakdown_text)

    def clear_database(self):
        if messagebox.askyesno("Clear Database", "Are you sure you want to clear all data?"):
            cursor.execute("DELETE FROM expenses")
            conn.commit()
            self.update_total_spent()
            messagebox.showinfo("Success", "Database cleared successfully!")

    def export_to_excel(self):
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()
        if not data:
            messagebox.showerror("Error", "No data to export!")
            return

        workbook = Workbook()
        sheet = workbook.active
        sheet.append(['ID', 'Description', 'Amount', 'Date'])
        for row in data:
            sheet.append(row)
        
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            workbook.save(file_path)
        
        category_workbook = Workbook()
        category_sheet = category_workbook.active
        cursor.execute("SELECT description, amount, date FROM expenses")
        category_data = cursor.fetchall()
        categories = {}
        
        for description, amount, date in category_data:
            category = categorize_expense(description)
            if category not in categories:
                categories[category] = []
            categories[category].append([description, amount, date])
        
        for category, rows in categories.items():
            category_sheet.append([category])
            for row in rows:
                category_sheet.append(row)
            category_sheet.append([])
        
        category_workbook.save(file_path.replace(".xlsx", "_categorized.xlsx"))
        messagebox.showinfo("Success", "Data exported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
