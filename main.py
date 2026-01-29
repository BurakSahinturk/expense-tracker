"""Main application controller"""

from expense_manager import ExpenseManager, categories
from storage import load_expenses, save_expenses
import tui_input
import cli_view

STORAGE_PATH = "expenses.csv"

ACTIONS = ["List Expenses", "Add an Expense", "Delete an Expense", "Show Summary", "Exit"]

def main():
    (expense_list, next_id) = load_expenses(STORAGE_PATH)
    manager = ExpenseManager(expense_list, next_id)
    print("Welcome!")
    
    # Main loop
    while True:
        # Get user action
        action = tui_input.get_main_action()
        
        # Handle "List Expenses"
        if action == "List Expenses":
            print(cli_view.show_expense_list(manager.export_expense_list()))
        
        # Handle "Add an Expense"
        elif action == "Add an Expense":
            expense_details = tui_input.get_expense_details()
            if expense_details is not None:
                try:
                    expense_id = manager.create_expense(expense_details["amount"], expense_details["category"], expense_details["description"], None)
                    save_expenses(STORAGE_PATH, manager.export_expense_list(), manager.next_id)
                    print(cli_view.show_expense_added(expense_id))
                except Exception as e:
                    print(cli_view.show_error(str(e)))
        
        # Handle "Delete an Expense"
        elif action == "Delete an Expense":
            expense_id = tui_input.get_expense_to_delete(manager.export_expense_list())
            if expense_id is not None:
                try:
                    manager.delete_expense(expense_id)
                    save_expenses(STORAGE_PATH, manager.export_expense_list(), manager.next_id)
                    print(cli_view.show_expense_deleted(expense_id))
                except Exception as e:
                    print(cli_view.show_error(str(e)))
            pass
        
        # Handle "Show Summary"
        elif action == "Show Summary":
            print(cli_view.show_category_summary(manager.get_category_summary()))
        
        # Handle "Exit"
        elif action == "Exit":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()