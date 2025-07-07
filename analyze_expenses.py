import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict
from tkinter import messagebox
import tkinter as tk

# Connect to SQLite database
conn = sqlite3.connect('budget.db')
cursor = conn.cursor()

def analyze_expenses():
    # Fetch all expenses from the database
    cursor.execute("SELECT description, amount FROM expenses")
    data = cursor.fetchall()

    if not data:
        messagebox.showerror("Error", "No data to analyze!")
        return

    # Categories dictionary to hold totals
    categories = defaultdict(float)

    # Categories to check against descriptions
    category_keywords = {
        'Food': ['food', 'restaurant', 'groceries', 'meal', 'طعام', 'أكل', 'غذاء', 'فطار'],
        'Drinks': ['drink', 'water', 'coffee', 'beverage', 'juice', 'شرب', 'مشروب', 'قهوة', 'مياه', 'عصير'],
        'Trans.': ['transport', 'trans', 'bus', 'taxi', 'uber', 'gas', 'car', 'مواصلات', 'توصيلة', 'سيارة', 'عربية'],
        'Clothes': ['cloth', 'shopping', 'apparel', 'هدوم', 'ملابس', 'تيشيرت', 'كسوة'],
        'Family': ['family', 'kids', 'school', 'عائلة', 'أسرة', 'اسرة', 'بيت'],
        'Hygiene': ['hygiene', 'صحة', 'نظافة', 'تنظيف', 'برفيوم', 'عطر'],       
        'Home': ['House', 'buildings', 'home', "جمعية", "جمعيه", 'الأثاث', 'الاثاث', 'المنزل', 'العزال'],
        'My Soul': ['روح الروح', 'روحي', 'حبيبتي' 'خطيبتي'],
        'Charity': ['handout', 'charity', "صدقة", "صدقه"],
        'Courses': ['course', 'درس', 'كورس'],
        'New Flat': ['الشقة', 'ايجار', 'إيجار'],
        'Others': []
    }

    # Categorize expenses
    categorized_expenses = defaultdict(list)  # Stores individual expenses per category
    for description, amount in data:
        found_category = False
        for category, keywords in category_keywords.items():
            if any(keyword.lower() in description.lower() for keyword in keywords):
                categories[category] += amount
                categorized_expenses[category].append((description, amount))  # Store details
                found_category = True
                break
        if not found_category:
            categories['Others'] += amount
            categorized_expenses['Others'].append((description, amount))

    # Plotting the results
    plot_categories(categories, categorized_expenses)

def plot_categories(categories, categorized_expenses):
    # Prepare data for plotting
    category_names = list(categories.keys())
    amounts = list(categories.values())

    fig, ax = plt.subplots()
    bars = ax.bar(category_names, amounts, color='skyblue')

    # Add labels inside the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height - 20,  # Adjust position slightly below the top of the bar
                f'{height:.2f}$', ha='center', va='bottom', color='black', fontsize=12)

    plt.xlabel('Categories')
    plt.ylabel('Amount Spent ($)')
    plt.title('Spending Analysis by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Function to handle click events on bars
    def on_bar_click(event):
        for bar, category in zip(bars, category_names):
            if bar.contains(event)[0]:  # Check if the mouse click was inside the bar
                show_expenses_popup(category, categorized_expenses[category])

    # Attach click event listener to figure
    fig.canvas.mpl_connect("button_press_event", on_bar_click)

    # Show the plot
    plt.show()

# Function to display expenses in a popup window
def show_expenses_popup(category, expenses):
    if not expenses:
        messagebox.showinfo("Expenses", f"No expenses recorded for {category}.")
        return

    popup = tk.Toplevel()
    popup.title(f"Expenses for {category}")
    
    text = tk.Text(popup, wrap="word", height=10, width=50)
    text.pack(padx=10, pady=10)

    text.insert(tk.END, f"Expenses for {category}:\n\n")
    for description, amount in expenses:
        text.insert(tk.END, f"- {description}: ${amount:.2f}\n")

    text.config(state="disabled")  # Make text read-only

# Call analyze_expenses to generate the analysis and interactive chart
#analyze_expenses()
