# Expense Manager
# Project 2 - Personal expense tracking system

import json
import os
from datetime import datetime
import csv

# File where expenses will be saved
EXPENSES_FILE = "expenses.json"
BUDGET = 500 # Monthly budget in euros

def load_expenses():
    """Load expenses from JSON file"""
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    """Save expanses to JSON file"""
    with open(EXPENSES_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4, ensure_ascii=False)

def show_menu():
    """Display the main menu"""
    print("\n" + "="*40)
    print("       EXPENSE MANAGER")
    print("="*40)
    print("1. Add expenses")
    print("2. Show all expenses")
    print("3. Show by category")
    print("4. Statistics")
    print("5. Search expenses")
    print("6. Check budget")
    print("7. Edit expense")
    print("8. Export to CSV")
    print("9. Delete expense")
    print("10. Exit")
    print("="*40)

def add_expense(expenses):
    """Add a new expense"""
    print("\n--- ADD NEW EXPENSE ---")
    
    #Pedir datos
    description = input("Description: ").strip()
    
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("\n❌ Invalid amount.")
        return
    
    category = input("Category (food/transport/entertainment/other): ").strip().lower()
    
    if description and amount > 0:
        new_expense = {
            "id": len(expenses) + 1,
            "description": description,
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        expenses.append(new_expense)
        save_expenses(expenses)
        print(f"\n✅ Expense added: €{amount:.2f} - {description}")
    else:
        print("\n❌ Invalid data.")

def show_expenses(expenses):
    """Show all expenses"""
    print("\n" + "="*50)
    print("       ALL EXPENSES")
    print("="*50)
    
    if not expenses:
        print("\n💰 No expenses yet. Add your first expense!")
    else:
        total = 0
        for expense in expenses:
            print(f"\n{expense['id']}. {expense['description']}")
            print(f"   💵 Amount: €{expense['amount']:.2f}")
            print(f"   📁 Category: {expense['category']}")
            print(f"   📅 Date: {expense['date']}")
            total += expense['amount']
            
        print("\n" + "-"*50)
        print(f"💰 TOTAL: €{total:.2f}")
        
    print("="*50)

def show_statistics(expenses):
    """Show statistics by category"""
    print("\n" + "="*40)
    print("       STATISTICS")
    print("="*40)
    
    if not expenses:
        print("\n💰 No expenses yet.")
        print("="*40)
        return
    
    # Calcular totales por categoría
    categories = {}
    total = 0
    
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount
        
        total += amount
        
        # Mostrar estadísticas
    print(f"\n💰 Total expenses: €{total:.2f}")
    print("\nBy category:")
        
    for category, amount in categories.items():
            percentage = (amount / total) * 100
            print(f"   📁 {category.capitalize()}: €{amount:.2f} ({percentage:.1f}%)")
            
    print("="*40)

def show_by_category(expenses):
    """Show expenses filtered by category"""
    if not expenses:
        print("\n💰 No expenses yet.")
        return
    category = input("\nEnter category (food/transport/entertainment/other): ").strip().lower()
    
    # Filtrar por categoría
    filtered = [exp for exp in expenses if exp['category'] == category]
    
    print("\n" + "="*50)
    print(f"      EXPENSES - {category.upper()}")
    print("="*50)
    
    if not filtered:
        print(f"\n❌ No expenses found in category '{category}'")
    else:
        total = 0
        for expense in filtered:
            print(f"\n{expense['id']}. {expense['description']}")
            print(f"   💵 Amount: €{expense['amount']:.2f}")
            print(f"   📅 Date: {expense['date']}")
            total += expense['amount']
            
        print("\n" + "-"*50)
        print(f"💰 TOTAL ({category}): €{total:.2f}")
        
    print("="*50)

def search_expenses(expenses):
    """Search expenses by keyword"""
    if not expenses:
        print("\n💰 No expenses yet.")
        return
    
    keyword = input("\nEnter keyword to search: ").strip().lower()
    
    if not keyword:
        print("\n❌ Please enter a keyword.")
        return
    
    # Find expenses containing keyword
    found = [exp for exp in expenses if keyword in exp['description'].lower()]
    
    print("\n" + "="*50)
    print(f"       SEARCH RESULTS: '{keyword}'")
    print("="*50)
    
    if not found:
        print(f"\n❌ No expenses found with keyword '{keyword}'")
    else:
        total = 0
        for expense in found:
            print(f"\n{expense['id']}. {expense['description']}")
            print(f"   💵 Amount: €{expense['amount']:.2f}")
            print(f"   📁 Category: {expense['category']}")
            print(f"   📅 Date: {expense['date']}")
            total += expense['amount']
            
        print("\n" + "-"*50)
        print(f"💰 TOTAL: €{total:.2f}")
    
    print("="*50)

def check_budget(expenses):
    """Check budget status"""
    total = sum(exp['amount'] for exp in expenses)
    remaining = BUDGET - total
    
    print("\n" + "="*40)
    print("       BUDGET STATUS")
    print("="*40)
    print(f"💰 Monthly budget: €{BUDGET:.2f}")
    print(f"📊 Current spending: €{total:.2f}")
    
    if remaining > 0:
        print(f"✅ Remaining: €{remaining:.2f}")
        
        # Warning if close to limit
        if remaining < BUDGET * 0.2: # Less than 20%
            print("⚠️ You're close to your budget limit!")
    else:
        print(f"❌ Exceeded by: €{abs(remaining):.2f}")
        print("⚠️ You've exceeded your monthly budget!")
        
    print("="*40)
    
def edit_expense(expenses):
    """Edit an existing expense"""
    show_expenses(expenses)
    
    if not expenses:
        return
    
    try:
        expense_id = int(input("\nEnter expense ID to edit: "))
        
        # Find expense by ID
        for expense in expenses:
            if expense["id"] == expense_id:
                print(f"\nEditing: {expense['description']}")
                print("\nWhat do you want to edit?")
                print("1. Description")
                print("2. Amount")
                print("3. Category")
                
                choice = input("\nSelect (1-3): ")
                
                if choice == "1":
                    new_desc = input("New description: ").strip()
                    if new_desc:
                        expense['description'] = new_desc
                        print("✅ Description updated!")
                
                elif choice == "2":
                    try:
                        new_amount = float(input("New amount: "))
                        if new_amount > 0:
                            expense['amount'] = new_amount
                            print("✅ Amount updated!")
                        else:
                            print("❌ Invalid amount.")
                    except ValueError:
                        print("❌ Invalid amount.")
                        
                elif choice == "3":
                    new_cat = input("New category (food/transport/entertainment/other): ").strip().lower()
                    expense['category'] = new_cat
                    print("✅  Category updated!")
                    
                else:
                    print("❌ Invalid option.")
                    return
                
                save_expenses(expenses)
                return
            print(f"\n❌ Expense with ID {expense_id} not found.")
    
    except ValueError:
            print("\n❌ Please enter a valid number.")

def export_to_csv(expenses):
    """Export expenses to CSV file"""
    if not expenses:
        print("\n💰 No expenses to export.")
        return
    filename = "expenses_export.csv"
    
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # Header row
            writer.writerow(["ID", "Description", "Amount", "Category", "Date"])
            
            # Data rows
            for exp in expenses:
                writer.writerow([
                    exp['id'],
                    exp['description'],
                    exp['amount'],
                    exp['category'],
                    exp['date']
                ])
        print(f"\n✅ Expenses exported to {filename}")
        print(f"📄 Total: {len(expenses)} expenses")
        
    except Exception as e:
        print(f"\n❌ Error exporting: {e}")
                               
def delete_expense(expenses):
    """Delete an expense"""
    show_expenses(expenses)
    
    if not expenses:
        return
    
    try:
        expense_id = int(input("\nEnter expense ID to delete: "))
        
        # Find and remove expense
        for i, expense in enumerate(expenses):
            if expense['id'] == expense_id:
                deleted = expenses.pop(i)
                save_expenses(expenses)
                print(f"\n🗑️ Expense deleted: {deleted['description']} - €{deleted['amount']:.2f}")
                return
        
        print(f"\n❌ Expense with ID {expense_id} not found.")
        
    except ValueError:
        print("\n❌ Please enter a valid number.")  
def main():
    """Main function"""
    expenses = load_expenses()
    
    while True:
        show_menu()
        option = input("\nSelect an option (1-10): ")
        
        if option == "1":
            add_expense(expenses)
        elif option == "2":
            show_expenses(expenses)
        elif option == "3":
            show_by_category(expenses)
        elif option == "4":
            show_statistics(expenses)
        elif option == "5":
            search_expenses(expenses)
        elif option == "6":
            check_budget(expenses)
        elif option == "7":
            edit_expense(expenses)
        elif option == "8":
            export_to_csv(expenses)
        elif option == "9":
            delete_expense(expenses)
        elif option == "10":
            print("\nGoodbye! 👋")
            break
        else:
            print("\n❌ Invalid option. Please try again.")

#Run the program
if __name__ == "__main__":
    main()
        