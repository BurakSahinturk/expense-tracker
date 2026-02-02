"""User input handling using inquirer"""

import inquirer
from inquirer import errors
from expense import Expense
from expense_manager import categories
import cli_view
from datetime import date as Date

ACTIONS = ["List Expenses",
           "Add an Expense",
           "Delete an Expense",
           "Correct an Expense",
           "Show Summary",
           "Exit"
]
CORRECTION_ACTIONS = [
    ("Amount", "amount"),
    ("Description", "description"),
    ("Category", "category"),
    ("Date", "date"),
    ("← Back", None),
]

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

def validate_day(answer, current):
    """Validate the day is a valid day"""
    if not current or not current.strip():
        raise errors.ValidationError("", reason="Day is needed")
    try:
        day = int(current)
        if day < 1 or day > 31:
            raise errors.ValidationError("", reason="Day must be valid number")
    except ValueError:
        raise errors.ValidationError("", reason="Day must be valid number")
    
def validate_year(answer, current):
    """VAlidate the year is a valid year"""
    if not current or not current.strip():
        raise errors.ValidationError("", reason="Year is needed")
    try:
        year = int(current)
        if year > Date.today().year:
            raise errors.ValidationError("", reason="Isn't it a bit early for that?")
    except ValueError:
        raise errors.ValidationError("", reason="Year must be a valid number")

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
        inquirer.Text("amount", message="Please enter the amount of the expense", validate=validate_amount),
        inquirer.List("category", message="Please select a category", choices=categories),
        inquirer.Text("description", message="Please enter the description for the expense", validate=validate_description)
    ]
    answers = inquirer.prompt(questions)
    answers["amount"] = float(answers["amount"]) #type: ignore
    return answers

def get_amount() -> float | None:
    questions = [inquirer.Text("amount", message="Please enter the corrected amount", validate=validate_amount)]
    return float(inquirer.prompt(questions)["amount"]) #type: ignore

def get_description() -> str | None:
    questions = [inquirer.Text("description", message="Please enter the correct description", validate=validate_description)]
    return float(inquirer.prompt(questions)["description"]) #type: ignore

def get_category() -> str | None:
    questions = [inquirer.List("category", message="Please select the correct category", choices=categories)]
    return inquirer.prompt(questions)["category"] #type: ignore

def get_date() -> Date | None:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    today = Date.today()
    questions = [
        inquirer.Text("day", message="Which day?", default=today.day, validate=validate_day),
        inquirer.List("month", message="Which month?", default=months[today.month - 1], choices=months),
        inquirer.Text("year", message="Which year?", default=today.year, validate=validate_year)
        ]
    while True:
        answers = inquirer.prompt(questions)
        try:
            day = int(answers["day"]) #type: ignore
            month = int(months.index(answers["month"])) + 1 #type: ignore
            year = int(answers["year"]) #type: ignore
            return Date(year, month, day)
        except ValueError:
            raise errors.ValidationError("", reason="Invalid calendar date")

def pick_expense(expenses: list[Expense], action: str) -> int | None:
    """Let user select an expense to process
    
    Args:
        expenses: List of Expense objects
    
    Returns:
        int: Selected expense ID or None if cancelled
    """
    
    message = f"Select an expense to {action}"

    final_expense_list = [(cli_view.format_expense_row(expense), expense.id) for expense in expenses]
    final_expense_list.append(("← Cancel", None)) # type: ignore

    questions = [inquirer.List("pick_expense", message=message, choices=final_expense_list)]
    return inquirer.prompt(questions)["pick_expense"] # type: ignore

def get_attribute_to_correct() -> str | None:
    """Let user select an expense attribute to correct"""
    questions = [
        inquirer.List(
            "attribute",
            message="Choose what to correct",
            choices=CORRECTION_ACTIONS
        )
    ]
    return inquirer.prompt(questions)["attribute"] # type: ignore

def confirm_action(message: str) -> bool:
    """Ask user yes/no confirmation

    Returns:
        bool: True if confirmed, False otherwise
    """
    return inquirer.confirm(message, default=False)