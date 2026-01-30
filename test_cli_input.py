# test_cli_input.py
import tui_input
from expense import Expense
from datetime import date

# Test 1: Validate amount
print("=== Test validate_amount ===")
class FakeAnswers:
    pass

try:
    tui_input.validate_amount(None, "15.50")
    print("✅ Valid amount accepted")
except:
    print("❌ Valid amount rejected")

try:
    tui_input.validate_amount(None, "-5")
    print("❌ Negative amount accepted")
except:
    print("✅ Negative amount rejected")

# Test 2: Get expense to delete
print("\n=== Test get_expense_to_delete ===")
expenses = [
    Expense(1, 15.50, "Groceries", "Pizza", date.today()),
    Expense(2, 45.00, "Transportation", "Uber", date.today())
]

result = tui_input.get_expense_to_delete(expenses)
print(f"Selected ID: {result}")

# Test 3: Confirm action
print("\n=== Test confirm_action ===")
confirmed = tui_input.confirm_action("Delete this expense?")
print(f"Confirmed: {confirmed}")