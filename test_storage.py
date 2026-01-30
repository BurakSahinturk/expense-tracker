from storage import save_expenses, load_expenses
from expense import Expense
from datetime import date

# Test 1: Save and load
expenses = [
    Expense(1, 15.50, "Groceries", "Pizza", date(2026, 1, 27)),
    Expense(2, 45.00, "Transportation", "Uber", date(2026, 1, 26))
]

save_expenses("test.csv", expenses, 3)
print("✅ Saved")

# Check the file manually
with open("test.csv") as f:
    print(f.read())

# Load back
loaded, next_id = load_expenses("test.csv")
print(f"✅ Loaded {len(loaded)} expenses, next_id={next_id}")

# Test 2: Load non-existent file
loaded2, next_id2 = load_expenses("nonexistent.csv")
print(f"✅ Non-existent file: {len(loaded2)} expenses, next_id={next_id2}")