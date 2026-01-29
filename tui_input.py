"""User input handling using inquirer"""

import inquirer
from inquirer import errors
from expense import Expense
from expense_manager import categories
import cli_view

ACTIONS = ["List Expenses", "Add an Expense", "Delete an Expense", "Show Summary", "Exit"]

def validate_amount(answers, current):
    """Validate amount is a positive number"""
    if not current or not current.strip():
        raise errors.ValidationError("", reason="Amount is needed")
    try:
        amount = float(current)
        if amount <= 0:
            raise errors.ValidationError("", reason="Amount must be a positive number")
        return True
    except ValueError:
        raise errors.ValidationError("", reason="Amount must be a valid number")
    
def validate_description(answers, current):
    """Validate description is not empty"""
    if not current or not current.strip():
        raise errors.ValidationError("", reason="Description is needed")
    return True

def get_main_action() -> str:
    """Display main menu and return selected action
    
    Returns:
        str: Selected action (e.g., "Add an Expense", "Exit")
    """
    questions = [
        inquirer.List("action", message="Choose an action", choices=ACTIONS) 
    ] #Actions come from the main to ensure single source of truth
    return inquirer.prompt(questions)["action"] # type: ignore

def get_expense_details() -> dict | None:
    """Prompt user for new expense details
    
    Returns:
        dict: {'amount': '15.50', 'category': 'Groceries', 'description': 'Pizza'}
        or None if user cancelled
    """
    questions = [
        inquirer.Text("amount", message="Please write the amount of the expense", validate=validate_amount),
        inquirer.List("category", message="Please select a category", choices=categories),
        inquirer.Text("description", message="Please write the description for the expense", validate=validate_description)
    ]
    return inquirer.prompt(questions)

def get_expense_to_delete(expenses: list[Expense]) -> int | None:
    """Let user select an expense to delete
    
    Args:
        expenses: List of Expense objects
    
    Returns:
        int: Selected expense ID or None if cancelled
    """
    final_expense_list = [(cli_view.format_expense_row(expense), expense.id) for expense in expenses]
    final_expense_list.append(("← Cancel", None))

    questions = [inquirer.List("expense_to_delete", message="Select an expense to delete", choices=final_expense_list)]
    return inquirer.prompt(questions)["expense_to_delete"] # type: ignore

def confirm_action(message: str) -> bool:
    """Ask user yes/no confirmation

    Returns:
        bool: True if confirmed, False otherwise
    """
    return inquirer.confirm(message, default=False)