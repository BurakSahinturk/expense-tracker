"""Service Layer"""

from expense import Expense, ExpenseDraft
from expense_manager import ExpenseManager
from datetime import date as Date
import storage

class ExpenseService:
    def __init__(self, manager: ExpenseManager, storage_path: str) -> None:
        self._manager = manager
        self._storage_path = storage_path
    
    def _save_draft(self, draft: ExpenseDraft) -> Expense:
        return storage.insert_expense(self._storage_path, draft)

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        date: Date | None = None
    ) -> int:
        draft= self._manager.create_draft(amount, category, description, date)
        new_expense = self._save_draft(draft)
        return self._manager.attach_expense(new_expense)
    
    def delete_expense(self, expense_id: int) -> None:
        storage.delete_expense(self._storage_path, expense_id)
        self._manager.delete_expense(expense_id)

    def correct_expense_amount(self, expense_id: int, new_amount: float) -> None:
        expense = self._manager.get_expense(expense_id)
        expense.correct_amount(new_amount)
        storage.update_expense_amount(self._storage_path, expense_id, new_amount)

    def recategorize_expense(self, expense_id: int, new_category: str) -> None:
        self._manager.recategorize_expense(expense_id, new_category)
        storage.update_expense_category(self._storage_path, expense_id, new_category)

    def correct_expense_date(self, expense_id: int, new_date: Date) -> None:
        expense = self._manager.get_expense(expense_id)
        expense.correct_date(new_date)
        storage.update_expense_date(self._storage_path, expense_id, new_date)

    def correct_expense_description(self, expense_id: int, new_description: str) -> None:
        expense = self._manager.get_expense(expense_id)
        expense.correct_description(new_description)
        storage.update_expense_description(self._storage_path, expense_id, new_description)

    def list_expenses(self) -> list[Expense]:
        return self._manager.export_expense_list()
    
    def get_category_summary(self):
        return self._manager.get_category_summary()
    
    def get_expense(self, expense_id: int) -> Expense:
        return self._manager.get_expense(expense_id)