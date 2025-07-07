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

# Define categories based on keywords
CATEGORY_KEYWORDS = {
    "Food": ["lunch", "dinner", "snack", "restaurant", "coffee", "groceries"],
    "Transport": ["bus", "taxi", "uber", "train", "fuel", "gas"],
    "Entertainment": ["movie", "game", "concert", "music"],
    "Bills": ["rent", "electricity", "water", "internet", "phone"],
    "Shopping": ["clothes", "shoes", "electronics", "furniture"],
    "Health": ["medicine", "doctor", "hospital", "pharmacy"],
    "Others": []
}

def categorize_expense(description):
    desc_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in desc_lower for keyword in keywords):
            return category
    return "Others"

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Budget Calculator")
        self.root.geometry("500x650")

        self.total_spent = tk.DoubleVar()
        self.amount = tk.DoubleVar()
        
        self.create_widgets()
        self.update_total_spent()

    def create_widgets(self):
        tk.Label(self.root, text="Description").pack(pady=5)
        self.description_text = tk.Text(self.root, height=2, width=40)
        self.description_text.pack(pady=5)

        tk.Label(self.root, text="Amount").pack(pady=5)
        self.amount_entry = tk.Entry(self.root, textvariable=self.amount)
        self.amount_entry.pack(pady=5)

        tk.Label(self.root, text="Select a Date").pack(pady=5)
        self.date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        tk.Button(self.root, text="Add Expense", command=self.add_expense).pack(pady=5)
        tk.Button(self.root, text="Calculate Total", command=self.calculate_total).pack(pady=5)
        tk.Button(self.root, text="Clear Database", command=self.clear_database, bg='red', fg='white').pack(pady=5)
        tk.Button(self.root, text="Export to Excel", command=self.export_to_excel).pack(pady=5)

        self.total_label = tk.Label(self.root, text="Total Spent: $0.00", font=("Arial", 12))
        self.total_label.pack(pady=20)

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
        self.total_spent.set(total)
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
        
        # Full expenses export
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Expenses"
        sheet.append(['ID', 'Description', 'Amount', 'Date'])
        for row in data:
            sheet.append(row)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            workbook.save(file_path)
            messagebox.showinfo("Success", "Full expenses exported successfully!")

        # Category-based export
        category_workbook = Workbook()
        category_sheet = category_workbook.active
        category_sheet.title = "Expenses By Category"
        categories = {}
        for _, desc, amount, date in data:
            category = categorize_expense(desc)
            if category not in categories:
                categories[category] = []
            categories[category].append((desc, amount, date))
        
        for category, expenses in categories.items():
            category_sheet.append([category])
            category_sheet.append(["Description", "Amount", "Date"])
            for expense in expenses:
                category_sheet.append(expense)
            category_sheet.append([])  # Space between categories
        
        file_path_category = file_path.replace(".xlsx", "_By_Category.xlsx")
        category_workbook.save(file_path_category)
        messagebox.showinfo("Success", "Category-wise expenses exported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
