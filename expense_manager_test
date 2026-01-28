from expense_manager import ExpenseManager
from datetime import date as Date

# Test 1: Create and edit
manager = ExpenseManager(None, 1)
exp_id = manager.create_expense(15.50, "Groceries", "Pizza", None)
print(f"Created: {exp_id}")

# Test 2: Correct amount
manager.correct_expense_amount(exp_id, 20.00)
expenses = manager.export_expense_list()
print(f"Updated amount: {expenses[0].amount}")

# Test 3: Recategorize
manager.recategorize_expense(exp_id, "Entertainment")
print(f"New category: {expenses[0].category}")

# Test 4: Invalid amount type
try:
    manager.create_expense("not a number", "Groceries", "Test", None) 
except Exception as e:
    print(f"Caught: {e}")

# Test 5: Non-existent expense
try:
    manager.delete_expense(999)
except Exception as e:
    print(f"Caught: {e}")