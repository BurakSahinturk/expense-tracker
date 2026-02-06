from fastapi import Depends
from expense_manager import ExpenseManager
from expense_service import ExpenseService
from storage import load_expenses
from config import STORAGE_PATH

# Singleton-style: create one manager and service for the app
_expense_list = load_expenses(STORAGE_PATH)
_manager = ExpenseManager(_expense_list)
_service = ExpenseService(_manager, STORAGE_PATH)

def get_expense_service() -> ExpenseService:
    return _service
