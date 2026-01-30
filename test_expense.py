from datetime import date as Date
from expense import Expense
from exceptions import InvalidExpenseDataError, InvalidExpenseIdError

# Test 1: Auto-date
print("=== Test 1: Auto-date ===")
exp1 = Expense(1, 15.50, "food", "Pizza")
print(f"Date: {exp1.date} (should be today)")

# Test 2: Manual date
print("\n=== Test 2: Manual date ===")
exp2 = Expense(2, 45.00, "transport", "Uber", Date(2026, 1, 20))
print(f"Date: {exp2.date} (should be 2026-01-20)")

# Test 3: CSV round-trip
print("\n=== Test 3: CSV round-trip ===")
row = exp1.to_csv_row()
print(f"CSV row: {row}")
exp3 = Expense.from_csv_row(row)
print(f"Loaded: ${exp3.amount} - {exp3.category} - {exp3.date}")
print(f"Match: {exp3.amount == exp1.amount and exp3.category == exp1.category}")

# Test 4: Invalid data
print("\n=== Test 4: Invalid amount ===")
try:
    bad_exp = Expense(1, 0, "food", "Free pizza")
except InvalidExpenseDataError as e:
    print(f"Caught error: {e}")

print("\n=== Test 5: Invalid ID ===")
try:
    bad_exp = Expense(-1, 10, "food", "Pizza")
except InvalidExpenseIdError as e:
    print(f"Caught error: {e}")

