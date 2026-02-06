"""Domain logic"""
from expense import Expense, ExpenseDraft
from datetime import date as Date
from exceptions import InvalidCategoryError, InvalidExpenseIdError, ExpenseNotFoundError

categories = ["Groceries", "Transportation", "Utilities", "Personal Care", "Savings", "Entertainment"]

class ExpenseManager:
    def __init__(self, expense_list: list[Expense] | None) -> None:
        if expense_list is None:
            self._ledger = {}
        else:
            self._ledger = {expense.id: expense for expense in expense_list}
        self._categories = categories
    
    def create_draft(self, amount: float, category: str, description: str, date: Date | None) -> ExpenseDraft:
        if category not in self._categories:
            raise InvalidCategoryError(f"Given category: {category} is not in predefined categories")
        return ExpenseDraft(amount, category, description, date)

    def attach_expense(self, new_expense: Expense) -> int:
        self._ledger[new_expense.id] = new_expense
        return new_expense.id

    def _get_existing_expense(self, expense_id: int) -> Expense:
        if not isinstance(expense_id, int):
            raise InvalidExpenseIdError(f"Expense ID must be an integer. Got {type(expense_id).__name__}")
        try:
            return self._ledger[expense_id]
        except KeyError:
            raise ExpenseNotFoundError(f"Expense #{expense_id} not found")
        
    def delete_expense(self, expense_id: int) -> None:
        self._get_existing_expense(expense_id)
        del self._ledger[expense_id]
    
    def export_expense_list(self) -> list[Expense]:
        return list(self._ledger.values())
    
    def correct_expense_amount(self, expense_id: int, new_amount: float) -> None:
        expense = self._get_existing_expense(expense_id)
        expense.correct_amount(new_amount)

    def correct_expense_date(self, expense_id: int, new_date: Date) -> None:
        expense = self._get_existing_expense(expense_id)
        expense.correct_date(new_date)

    def correct_expense_description(self, expense_id: int, new_description: str) -> None:
        expense = self._get_existing_expense(expense_id)
        expense.correct_description(new_description)

    def validate_category(self, new_category: str) -> None:
        if new_category.strip() not in self._categories:
            raise InvalidCategoryError(f"Given category: {new_category} is not in predefined categories")

    def recategorize_expense(self, expense_id: int, new_category: str) -> None:
        expense = self._get_existing_expense(expense_id)
        new_category = new_category.strip()
        self.validate_category(new_category)
        expense.recategorize(new_category)
    
    def get_category_summary(self) -> dict:
        category_totals = {category: float(0) for category in self._categories}
        for expense in self.export_expense_list():
                category_totals[expense.category] += expense.amount
        return category_totals
    
    def get_expense(self, expense_id: int) -> Expense:
        expense = self._get_existing_expense(expense_id)
        return expense