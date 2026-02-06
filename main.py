"""Main application controller"""

from expense import Expense
from expense_manager import ExpenseManager
from expense_service import ExpenseService
from storage import load_expenses, create_table
import tui_input
import cli_view
from exceptions import ExpenseNotFoundError, InvalidExpenseIdError, InvalidExpenseDataError
from config import STORAGE_PATH

def correct_amount(service: ExpenseService, expense_id: int, expense: Expense) -> None:
    print(cli_view.show_current_amount(expense.amount))
    new_amount = tui_input.get_amount()
    if new_amount is not None:
        service.correct_expense_amount(expense_id, new_amount)

def correct_description(service: ExpenseService, expense_id: int, expense: Expense) -> None:
    print(cli_view.show_current_description(expense.description))
    new_description = tui_input.get_description()
    if new_description is not None:
        service.correct_expense_description(expense_id, new_description)

def correct_category(service: ExpenseService, expense_id: int, expense: Expense) -> None:
    print(cli_view.show_current_category(expense.category))
    new_category = tui_input.get_category()
    if new_category is not None:
        service.recategorize_expense(expense_id, new_category)

def correct_date(service: ExpenseService, expense_id: int, expense: Expense) -> None:
    print(cli_view.show_current_date(expense.date))
    new_date = tui_input.get_date()
    if new_date is not None:
        service.correct_expense_date(expense_id, new_date)
        
CORRECTION_HANDLERS = {
    "amount": correct_amount,
    "description": correct_description,
    "category": correct_category,
    "date": correct_date,
}

def main():
    create_table(STORAGE_PATH)
    (expense_list) = load_expenses(STORAGE_PATH)
    manager = ExpenseManager(expense_list)
    service = ExpenseService(manager, STORAGE_PATH)

    print(cli_view.show_welcome()) 

    # Main loop
    while True:
        # Get user action
        action = tui_input.get_main_action()
        
        # Handle "List Expenses"
        if action == "List Expenses":
            expense_list = service.list_expenses()
            print(cli_view.show_expense_list(expense_list))
        
        # Handle "Add an Expense"
        elif action == "Add an Expense":
            expense_details = tui_input.get_expense_details()
            if expense_details is not None:
                try:
                    expense_id = service.add_expense(
                        float(expense_details["amount"]),
                        expense_details["category"],
                        expense_details["description"],
                        None)
                    print(cli_view.show_expense_added(expense_id))
                except Exception as e:
                    print(cli_view.show_error(str(e)))
        
        # Handle "Delete an Expense"
        elif action == "Delete an Expense":
            expense_id = tui_input.pick_expense(service.list_expenses(), "delete")
            if expense_id is not None:
                if tui_input.confirm_action(f"Delete expense #{expense_id}?"):
                    try:
                        service.delete_expense(expense_id)
                        print(cli_view.show_expense_deleted(expense_id))
                    except (ExpenseNotFoundError, InvalidExpenseIdError, InvalidExpenseDataError, ) as e:
                        print(cli_view.show_error(str(e)))
                else:
                    print(cli_view.show_expense_delete_cancelled())
        
        # Handle "Correct an Expense"
        elif action == "Correct an Expense":
            expense_id = tui_input.pick_expense(service.list_expenses(), "correct")
            if expense_id is None:
                continue
            expense = service.get_expense(expense_id)
            while True:
                attribute = tui_input.get_attribute_to_correct()
                if attribute is None:
                    break
                handler = CORRECTION_HANDLERS.get(attribute)
                if handler is None:
                    continue
                try:
                    handler(service, expense_id, expense)
                    print(cli_view.show_expense_corrected(expense_id))
                except (ExpenseNotFoundError, InvalidExpenseIdError, InvalidExpenseDataError) as e:
                    print(cli_view.show_error(str(e)))

        # Handle "Show Summary"
        elif action == "Show Summary":
            summary_dict = service.get_category_summary()
            print(cli_view.show_category_summary(summary_dict))
        
        # Handle "Exit"
        elif action == "Exit":
            print(cli_view.show_goodbye())
            break

if __name__ == "__main__":
    main()