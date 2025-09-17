import sqlite3
from tkinter import messagebox, filedialog
import tkinter as tk
from openpyxl import Workbook
from analyze_expenses import category_keywords # Import category_keywords
from config import DATABASE_NAME # Import DATABASE_NAME
import logging # Import logging
from collections import defaultdict # Import defaultdict

# Configure logging for analyze_expenses_002
logging.basicConfig(filename='budget_app.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Connect to SQLite database
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

def export_to_excel():
    """Exports expenses to an Excel file with a main sheet and separate category sheets."""
    try:
        cursor.execute("SELECT description, amount, date FROM expenses")
        data = cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error in export_to_excel: {e}")
        messagebox.showerror("Database Error", "Could not retrieve expenses for export.")
        return

    if not data:
        messagebox.showerror("Error", "No data to export!")
        return

    # Categorize expenses
    categorized_expenses = defaultdict(list)
    for description, amount, date in data:
        category = "Others"
        for cat, keywords in category_keywords.items():
            if any(keyword.lower() in description.lower() for keyword in keywords):
                category = cat
                break
        categorized_expenses[category].append((date, description, amount))

    # File save dialog
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel Files", "*.xlsx")],
                                             title="Save as")
    if not file_path:
        return

    # Create an Excel workbook
    workbook = Workbook()
    main_sheet = workbook.active
    main_sheet.title = "Main"

    # Add headers
    main_sheet.append(["Date", "Description", "Amount", "Category"])

    # Fill main sheet and category sheets
    for category, expenses in categorized_expenses.items():
        for date, description, amount in expenses:
            main_sheet.append([date, description, amount, category])  # Add to main sheet
        
        # Create a separate sheet for each category
        sheet = workbook.create_sheet(title=category)
        sheet.append(["Date", "Description", "Amount"])  # Headers
        for date, description, amount in expenses:
            sheet.append([date, description, amount])

    # Save workbook
    try:
        workbook.save(file_path)
        messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
    except Exception as e:
        logging.error(f"Error saving Excel file: {e}")
        messagebox.showerror("Error", f"Failed to save Excel file: {e}")
