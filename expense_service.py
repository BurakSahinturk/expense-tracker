"""Service Layer"""

from expense import Expense
from expense_manager import ExpenseManager
from datetime import date as Date
from storage import save_expenses

class ExpenseService:
    def __init__(self, manager: ExpenseManager, storage_path: str) -> None:
        self._manager = manager
        self._storage_path = storage_path
    
    def _persist(self) -> None:
        save_expenses(
            self._storage_path,
            self._manager.export_expense_list(),
            self._manager.next_id
            )

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        date: Date | None = None
    ) -> int:
        expense_id = self._manager.create_expense(amount, category, description, date)
        self._persist()
        return expense_id

    def delete_expense(self, expense_id: int) -> None:
        self._manager.delete_expense(expense_id)
        self._persist()

    def correct_expense_amount(self, expense_id: int, new_amount: float) -> None:
        self._manager.correct_expense_amount(expense_id, new_amount)
        self._persist()

    def recategorize_expense(self, expense_id: int, new_category: str) -> None:
        self._manager.recategorize_expense(expense_id, new_category)
        self._persist()

    def correct_expense_date(self, expense_id: int, new_date: Date) -> None:
        self._manager.correct_expense_date(expense_id, new_date)
        self._persist()

    def correct_expense_description(self, expense_id: int, new_description: str) -> None:
        self._manager.correct_expense_description(expense_id, new_description)
        self._persist()

    def list_expenses(self) -> list[Expense]:
        return self._manager.export_expense_list()
    
    def get_category_summary(self):
        return self._manager.get_category_summary()