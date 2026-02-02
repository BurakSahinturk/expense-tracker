# test_expense.py
import unittest
from datetime import date as Date
from expense import Expense
from expense import (
    InvalidExpenseIdError,
    InvalidExpenseDataError,
    InvalidCategoryError,
    InvalidExpenseDescriptionError
)

class TestExpense(unittest.TestCase):
    """Unit tests for Expense class"""

    def test_happy_path(self):
        """Expense is created correctly"""
        exp = Expense(1, 25.0, "Groceries", "Lunch", Date.today())
        self.assertIsInstance(exp, Expense)
        self.assertEqual(exp.id, 1)
        self.assertEqual(exp.amount, 25.0)
        self.assertEqual(exp.category, "Groceries")
        self.assertEqual(exp.description, "Lunch")
        self.assertEqual(exp.date, Date.today())

    def test_auto_date(self):
        """If date is None, today is assigned"""
        exp = Expense(2, 15.50, "Food", "Pizza")
        self.assertEqual(exp._date, Date.today())

    def test_invalid_ids(self):
        """Invalid expense IDs should raise InvalidExpenseIdError"""
        invalid_ids = [None, "a", 0, -5]
        for invalid_id in invalid_ids:
            with self.assertRaises(InvalidExpenseIdError):
                Expense(invalid_id, 10.0, "Food", "Snack", Date.today())

    def test_invalid_amounts(self):
        """Invalid amounts should raise InvalidExpenseDataError"""
        invalid_amounts = [None, "abc", 0, -10]
        for amount in invalid_amounts:
            with self.assertRaises(InvalidExpenseDataError):
                Expense(1, amount, "Food", "Snack", Date.today())

    def test_invalid_category(self):
        """Empty or None category should raise InvalidCategoryError"""
        invalid_categories = [None, ""]
        for cat in invalid_categories:
            with self.assertRaises(InvalidCategoryError):
                Expense(1, 10.0, cat, "Snack", Date.today())

    def test_invalid_description(self):
        """Empty or None description should raise InvalidExpenseDescriptionError"""
        invalid_descriptions = [None, ""]
        for desc in invalid_descriptions:
            with self.assertRaises(InvalidExpenseDescriptionError):
                Expense(1, 10.0, "Food", desc, Date.today())

if __name__ == "__main__":
    unittest.main()