"""Display formatting functions"""

from expense import Expense

def show_expense_added(expense_id: int) -> str:
    """Return success message for added expense"""
    return f"Expense [{expense_id}] is successfully added"

def show_expense_deleted(expense_id: int) -> str:
    """Return success message for deleted expense"""
    return f"Expense [{expense_id}] is successfully deleted"

def show_expense_delete_cancelled() -> str:
    """Return cancellation message for quitting during deleting"""
    return f"Deletion cancelled"

def show_expense_list(expenses: list[Expense]) -> str:
    """Format list of expenses as ASCII table"""
    if not expenses:
        return show_empty_list()

    max_width_category = 9
    max_width_description = 11
    for expense in expenses:
        if len(expense.category) > max_width_category:
            max_width_category = len(expense.category)
        if len(expense.description) > max_width_description:
            max_width_description = len(expense.description)

    max_width_description += 2
    max_width_category += 2
    mw_id = 4
    mw_amount = 10
    mw_date = 10

    def format_table_row(expense: Expense):
        formatted_amount = f"${expense.amount:.2f}"
        return f"{expense.id:<{mw_id}} | {formatted_amount:>{mw_amount}} | {expense.category:<{max_width_category}} | {expense.description:<{max_width_description}} | {expense.date}"
    
    header_row = f"{'ID':<{mw_id}} | {'Amount':^{mw_amount}} | {'Category':^{max_width_category}} | {'Description':^{max_width_description}} | {'Date':^{mw_date}}"
    separator_row = f"{'-'*mw_id}-|-{'-' * mw_amount}-|-{'-' * max_width_category}-|-{'-' * max_width_description}-|-{'-'*mw_date}"
    expenses_table_data = "\n".join([format_table_row(expense) for expense in expenses])
    return header_row + "\n" + separator_row + "\n" + expenses_table_data

def show_total(total: float) -> str:
    """Format total spending message"""
    return f"💰 Total spending: ${total:.2f}"

def show_category_summary(category_totals: dict) -> str:
    """Format category breakdown
    
    Args:
        category_totals: {'Groceries': 23.50, 'Transportation': 45.00}
    
    Should look like:
    Groceries: $23.50
    Transportation: $45.00
    ---
    Total: $68.50
    """
    total_sum = 0
    summary = ""
    for category in category_totals:
        total_sum += category_totals[category]
        summary += f"{category}: ${category_totals[category]:.2f}\n"
    return summary + f"---\nTotal: ${total_sum:.2f}"

def show_error(message: str) -> str:
    """Format error message"""
    return f"❌ Error: {message}"

def show_empty_list() -> str:
    """Message for empty expense list"""
    return "📭 No expenses yet!"

def format_expense_row(expense: Expense) -> str:
    return f"[{expense.id}] ${expense.amount:.2f} - {expense.category} - {expense.description}"


# print(show_expense_list(None))

# expense1 = Expense(1, 40.3, "Groceries", "Pizza with extra topping")
# expense2 = Expense(2, 30, "Transportaion", "Über")
# print(show_expense_list([expense1, expense2]))