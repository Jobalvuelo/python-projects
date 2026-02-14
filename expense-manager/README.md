# Expense Manager

A professional command-line expense tracking application built with Python.

## Features

- ✅ **Add expenses** - Track your spending with automatic timestamps
- 📋 **View all expenses** - See all expenses with total amount
- 📁 **Filter by category** - View expenses by category (food, transport, entertainment, other)
- 📊 **Statistics** - Detailed breakdown by category with percentages
- 🔍 **Search** - Find expenses by keyword
- 💰 **Budget tracking** - Monitor spending against monthly budget (€500)
- ✏️ **Edit expenses** - Update description, amount, or category
- 📄 **Export to CSV** - Export data to Excel-compatible format
- 🗑️ **Delete expenses** - Remove unwanted entries
- 💾 **Data persistence** - All data saved in JSON format

## How to Run
```bash
cd src
python expense_manager.py
```

## Menu Options

1. Add expense
2. Show all expenses
3. Show by category
4. Statistics
5. Search expenses
6. Check budget
7. Edit expense
8. Export to CSV
9. Delete expense
10. Exit

## Technologies

- Python 3
- JSON for data storage
- CSV for data export
- datetime for timestamps

## Project Structure
```
expense-manager/
├── src/
│   ├── expense_manager.py    # Main application
│   ├── expenses.json          # Data storage (auto-generated)
│   └── expenses_export.csv    # Export file (auto-generated)
└── README.md                  # Documentation
```

## Budget Feature

Set your monthly budget in the code:
```python
BUDGET = 500  # Monthly budget in euros
```

The app will warn you when:
- You're close to budget limit (< 20% remaining)
- You've exceeded your budget

## Author

**Ayoub Hamouiat**
- Location: Switzerland
- Learning: Python Development
- Goal: Junior Developer Position

## Date

Created: February 2026