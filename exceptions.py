"""Custom Exceptions"""

class InvalidExpenseIdError(Exception):
    """Raised when an expense ID is empty or invalid"""
    pass

class InvalidCategoryError(Exception):
    """Raised when an expense category is empty or invalid"""
    pass

class InvalidExpenseDataError(Exception):
    """Raised when expense amount is empty or invalid"""
    pass

class InvalidExpenseDescriptionError(Exception):
    """Raised when an expense description is empty or invalid"""
    pass

class InvalidDateError(Exception):
    """Raised when a date is invalid"""
    pass

class ExpenseNotFoundError(Exception):
    """Raised when there are no expense found with the given ID"""
    pass

class CorruptedDataError(Exception):
    """Raised when trying to load a corrupted file"""
    pass