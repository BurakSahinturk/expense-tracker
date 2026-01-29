"""Domain logic"""
from expense import Expense
from datetime import date as Date
from exceptions import InvalidCategoryError, InvalidExpenseIdError, ExpenseNotFoundError

categories = ["Groceries", "Transportation", "Utilities", "Personal Care", "Savings", "Entertainment"]

class ExpenseManager:
    def __init__(self, expense_list: list[Expense] | None, next_id: int) -> None:
        if expense_list is None:
            self._ledger = {}
        else:
            self._ledger = {expense.id: expense for expense in expense_list}
        self._next_id = next_id
        self._categories = categories
    
    @property
    def next_id(self):
        return self._next_id
    
    def create_expense(self, amount: float, category: str, description: str, date: Date | None) -> int:
        if category not in self._categories:
            raise InvalidCategoryError(f"Given category: {category} is not in predefined categories")
        expense_id = self._next_id
        new_expense = Expense(expense_id, amount, category, description, date)
        self._ledger[expense_id] = new_expense
        self._next_id += 1
        return expense_id

    def _get_existing_expense(self, expense_id: int) -> Expense:
        try:
            return self._ledger[expense_id]
        except KeyError:
            raise ExpenseNotFoundError(f"Expense with id: {expense_id} not found")
        
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

    def recategorize_expense(self, expense_id: int, new_category: str) -> None:
        expense = self._get_existing_expense(expense_id)
        if new_category not in self._categories:
            raise InvalidCategoryError(f"Given category: {new_category} is not in predefined categories")
        expense.recategorize(new_category)
    
    def get_category_summary(self) -> dict:
        category_totals = {category: float(0) for category in self._categories}
        for expense in self.export_expense_list():
                category_totals[expense.category] += expense.amount
        return category_totals