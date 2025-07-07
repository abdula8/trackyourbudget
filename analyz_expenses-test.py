import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import sqlite3

# Function to get expenses from the database based on category
def get_expenses_by_category(category):
    conn = sqlite3.connect("budget.db")  # Update with your actual database file
    cursor = conn.cursor()
    cursor.execute("SELECT amount, description, date FROM expenses WHERE category=?", (category,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# Function to display expenses in a popup window
def show_expenses_popup(category):
    expenses = get_expenses_by_category(category)
    
    if not expenses:
        messagebox.showinfo("Expenses", f"No expenses recorded for {category}.")
        return

    popup = tk.Toplevel()
    popup.title(f"Expenses for {category}")

    text = tk.Text(popup, wrap="word", height=10, width=50)
    text.pack(padx=10, pady=10)

    text.insert(tk.END, f"Expenses for {category}:\n\n")
    for amount, description, date in expenses:
        text.insert(tk.END, f"- {date}: {description} (${amount})\n")

    text.config(state="disabled")  # Make text read-only

# Function to handle click events on bars
def on_bar_click(event):
    for bar, category in zip(bars, categories):
        if bar.contains(event)[0]:  # Check if the mouse click was inside the bar
            show_expenses_popup(category)

# Sample Data (Modify if needed)
categories = ["Food", "Clothes", "Drinks", "Trans.", "Others", "Hygiene", "Family", "My Soul", "Courses", "Charity"]
amounts = [1045, 2050, 540, 851, 1730, 5, 296, 1672, 250, 220]

# Create the bar chart
fig, ax = plt.subplots()
bars = ax.bar(categories, amounts, color="skyblue")

# Attach click event listener to figure
fig.canvas.mpl_connect("button_press_event", on_bar_click)

ax.set_title("Spending Analysis by Category")
ax.set_ylabel("Amount Spent ($)")

plt.xticks(rotation=45)
plt.show()
