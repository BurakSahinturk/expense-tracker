"""Test Unit for Expense Manager"""

import unittest
from expense import Expense
from expense_manager import ExpenseManager, categories
from datetime import date as Date
from exceptions import (
    ExpenseNotFoundError,
    InvalidExpenseIdError
)

class TestExpenseManager(unittest.TestCase):
    """Unit tests for Expense Manager"""

    #Set Up:
    def setUp(self) -> None:
        self.manager = ExpenseManager([], 1)
        self.exp1_id = self.manager.create_expense(15.50, categories[0], "Pizza", None)
        self.exp1 = self.manager.get_expense(self.exp1_id) 

    # Happy Paths
    def test_manager_creates_expense(self):
        """Manager can create an expense successfully"""
        self.assertEqual(self.exp1.id, 1)
    
    def test_manager_corrects_expense_amount(self):
        """Manager can correct the amount"""
        self.manager.correct_expense_amount(self.exp1_id, 13)
        self.assertEqual(self.exp1.amount, 13)

    def test_manager_recategorizes_expense(self):
        """Manager can change the category of an expense"""
        self.manager.recategorize_expense(self.exp1_id, "Utilities")
        self.assertEqual(self.exp1.category, "Utilities")

    def test_manager_corrects_expense_description(self):
        """Manager can change the description of an expense"""
        self.manager.correct_expense_description(self.exp1_id, "Water bill")
        self.assertEqual(self.exp1.description, "Water bill")

    def test_manager_corrects_date(self):
        """Manager can change the date of an expense"""
        random_date = Date(2006, 9, 9)
        self.manager.correct_expense_date(self.exp1_id, random_date)
        self.assertEqual(self.exp1.date, random_date)

    def test_manager_exports_expense_list(self):
        """Manager can export a list of expenses"""
        expense_list = self.manager.export_expense_list()
        self.assertEqual(len(expense_list), 1)
        self.assertIn(self.exp1, expense_list)

    def test_manager_deletes_expense(self):
        """Manager can delete an expense"""
        exp2_id = self.manager.create_expense(22, "Personal Care", "Shampoo", None)
        self.assertEqual(len(self.manager.export_expense_list()), 2)
        self.manager.delete_expense(exp2_id)
        self.assertEqual(len(self.manager.export_expense_list()), 1)

    def test_manager_exports_category_summary(self):
        category_dict = self.manager.get_category_summary()
        self.assertIsInstance(category_dict, dict)
        self.assertEqual(category_dict[categories[0]], 15.5)
        self.assertEqual(category_dict[categories[1]], 0)
    
    # Unhappy Paths
    def test_not_existing_id_for_get_expense_raises(self):
        """Test calling get_expense with a non-existing expense ID raises custom Exception"""
        with self.assertRaises(ExpenseNotFoundError):
            self.manager.get_expense(999)

    def test_invalid_id_caller(self):
        """Test calling any expense with invalid ID raises custom Exception"""
        invalid_ids = [None, "abc"]
        for ii in invalid_ids:
            with self.assertRaises(InvalidExpenseIdError):
                self.manager.get_expense(ii)
    
    def test_delete_twice_raises(self):
        """Deleting the same expense twice raises ExpenseNotFoundError"""
        exp_id = self.manager.create_expense(10, categories[0], "Snack", None)
        self.manager.delete_expense(exp_id)
        with self.assertRaises(ExpenseNotFoundError):
            self.manager.delete_expense(exp_id)

    def test_create_expense_creates_and_stores_expense(self):
        exp_id = self.manager.create_expense(
            20.0,
            categories[0],
            "Lunch",
            None
        )

        expense = self.manager.get_expense(exp_id)

        self.assertEqual(expense.id, exp_id)
        self.assertEqual(expense.amount, 20.0)
        self.assertEqual(expense.category, categories[0])
        self.assertEqual(expense.description, "Lunch")


    def test_create_expense_increments_id(self):
        exp1_id = self.manager.create_expense(10, categories[0], "Coffee", None)
        exp2_id = self.manager.create_expense(5, categories[1], "Movie", None)

        self.assertEqual(exp1_id + 1, exp2_id)

    def test_category_summary_contains_all_categories(self):
        summary = self.manager.get_category_summary()

        for category in categories:
            self.assertIn(category, summary)


    def test_category_summary_single_expense(self):
        summary = self.manager.get_category_summary()

        self.assertEqual(summary[categories[0]], 15.5)


    def test_category_summary_multiple_expenses_same_category(self):
        self.manager.create_expense(10, categories[0], "Snack", None)

        summary = self.manager.get_category_summary()

        self.assertEqual(summary[categories[0]], 25.5)


    def test_category_summary_multiple_categories(self):
        self.manager.create_expense(30, categories[1], "Concert", None)

        summary = self.manager.get_category_summary()

        self.assertEqual(summary[categories[0]], 15.5)
        self.assertEqual(summary[categories[1]], 30)

if __name__ == "__main__":
    unittest.main()