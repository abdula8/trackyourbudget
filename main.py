import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
from datetime import datetime
from openpyxl import Workbook
from tkcalendar import DateEntry
from analyze_expenses import analyze_expenses  # Import the analysis function

# Database Setup
conn = sqlite3.connect('budget.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    amount REAL,
                    category TEXT,
                    date TEXT)''')
conn.commit()

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Budget Calculator")
        self.root.geometry("550x650")
        self.root.configure(bg="#f4f4f4")

        # Variables
        self.amount = tk.DoubleVar()
        self.categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]

        # UI Setup
        self.create_widgets()
        self.update_total_spent()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        tk.Label(frame, text="Description:", font=("Arial", 12)).pack(anchor="w")
        self.description_text = tk.Entry(frame, width=40)
        self.description_text.pack(pady=5)
        
        tk.Label(frame, text="Amount ($):", font=("Arial", 12)).pack(anchor="w")
        self.amount_entry = tk.Entry(frame, textvariable=self.amount, width=20)
        self.amount_entry.pack(pady=5)
        
        tk.Label(frame, text="Category:", font=("Arial", 12)).pack(anchor="w")
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(frame, textvariable=self.category_var, values=self.categories, state="readonly")
        self.category_dropdown.pack(pady=5)
        
        tk.Label(frame, text="Select a Date:", font=("Arial", 12)).pack(anchor="w")
        self.date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        tk.Button(frame, text="Add Expense", command=self.add_expense, bg="#5cb85c", fg="white").pack(pady=5, fill="x")
        tk.Button(frame, text="Calculate Total", command=self.calculate_total, bg="#0275d8", fg="white").pack(pady=5, fill="x")
        tk.Button(frame, text="Analyze Expenses", command=analyze_expenses, bg="#f0ad4e", fg="white").pack(pady=5, fill="x")
        tk.Button(frame, text="Clear Database", command=self.clear_database, bg='red', fg='white').pack(pady=5, fill="x")
        tk.Button(frame, text="Export to Excel", command=self.export_to_excel, bg="#0275d8", fg="white").pack(pady=5, fill="x")

        self.total_label = tk.Label(frame, text="Total Spent: $0.00", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=10)

    def add_expense(self):
        description = self.description_text.get()
        amount = self.amount.get()
        category = self.category_var.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not description or amount <= 0 or not category:
            messagebox.showerror("Error", "Please enter valid details.")
            return

        cursor.execute("INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)",
                       (description, amount, category, date))
        conn.commit()
        self.description_text.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.update_total_spent()

    def update_total_spent(self):
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0.0
        self.total_label.config(text=f"Total Spent: ${total:.2f}")

    def calculate_total(self):
        selected_date = self.date_entry.get_date().strftime('%Y-%m-%d')
        cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE DATE(date) = ? GROUP BY category", (selected_date,))
        data = cursor.fetchall()
        
        if not data:
            messagebox.showinfo("No Data", f"No expenses found for {selected_date}")
            return
        
        breakdown = f"Expenses on {selected_date}:\n"
        for category, amount in data:
            breakdown += f"{category}: ${amount:.2f}\n"
        
        messagebox.showinfo("Total Expense", breakdown)

    def clear_database(self):
        if messagebox.askyesno("Clear Database", "Are you sure?"):
            cursor.execute("DELETE FROM expenses")
            conn.commit()
            self.update_total_spent()
            messagebox.showinfo("Success", "Database cleared!")

    def export_to_excel(self):
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()

        if not data:
            messagebox.showerror("Error", "No data to export!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[["Excel files", "*.xlsx"]])
        if file_path:
            # Export Full Data
            wb = Workbook()
            sheet = wb.active
            sheet.append(["ID", "Description", "Amount", "Category", "Date"])
            for row in data:
                sheet.append(row)
            wb.save(file_path)
            
            # Export By Category
            wb_category = Workbook()
            sheet_category = wb_category.active
            categories = set(row[3] for row in data)
            sheet_category.append(["Date"] + list(categories))
            
            for row in data:
                date, category, amount = row[4], row[3], row[2]
                row_data = [date] + [amount if c == category else "" for c in categories]
                sheet_category.append(row_data)
            
            category_file_path = file_path.replace(".xlsx", "_By_Category.xlsx")
            wb_category.save(category_file_path)
            
            messagebox.showinfo("Success", "Exported Successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
