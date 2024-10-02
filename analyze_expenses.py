import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict
from tkinter import messagebox

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
        'Food': ['food', 'restaurant', 'groceries', 'meal'],
        'Drinks': ['drink', 'water', 'coffee', 'beverage', 'juice'],
        'Transportation': ['transport', 'bus', 'taxi', 'uber', 'gas', 'car'],
        'Clothes': ['cloth', 'shopping', 'apparel'],
        'Family': ['family', 'kids', 'school'],
        'Health': ['health', 'hygene'],       
        'Home': ['House', 'buildings', "جمعية", "جمعيه"],       
        'Charity': ['handout', 'charity', "صدقة", "صدقه"],
        'Courses': ['course', 'درس', 'كورس'],
        'Others': []
    }

    # Categorize expenses
    for description, amount in data:
        found_category = False
        for category, keywords in category_keywords.items():
            if any(keyword.lower() in description.lower() for keyword in keywords):
                categories[category] += amount
                found_category = True
                break
        if not found_category:
            categories['Others'] += amount

    # Plotting the results
    plot_categories(categories)

def plot_categories(categories):
    # Prepare data for plotting
    category_names = list(categories.keys())
    amounts = list(categories.values())

    # plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()#figsize=(8, 6), layout='constrained')
    bars = ax.bar(category_names, amounts, color='skyblue')
    # plt.bar(category_names, amounts, color='blue')
    # Add labels on the right side of the bars (outside)
    # Add labels inside the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height - 20,  # Adjust position slightly below the top of the bar
                f'{height:.2f}$', ha='center', va='bottom', color='black', fontsize=12)

    plt.xlabel('Categories')
    plt.ylabel('Amount Spent ($)')
    plt.title('Spending Analysis by Category')
    plt.tight_layout()

    # Show the plot
    plt.show()
