"""Expense entity representing an expense."""

from datetime import date as Date
from exceptions import InvalidExpenseIdError, InvalidExpenseDataError, InvalidExpenseDescriptionError, InvalidCategoryError, InvalidDateError

class Expense:
    def __init__(
            self,
            expense_id: int,
            amount: float,
            category: str,
            description: str,
            date: Date | None = None
            ) -> None:
        
        #Validation
        if expense_id < 1:
            raise InvalidExpenseIdError(f"Expense ID must be a positive integer. Got {expense_id} instead")
        if not category:
            raise InvalidCategoryError("Category must be a non-empty string")
        if not description:
            raise InvalidExpenseDescriptionError("Description must be a non-empty string")
        if date is None:
            date = Date.today()
        validated_amount = self._normalize_amount(amount)
        
        self._id = expense_id
        self._amount = validated_amount
        self._category = category
        self._description = description
        self._date = date

    def _normalize_amount(self, amount: float|int) -> float:
        if not isinstance(amount, float):
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                raise InvalidExpenseDataError(f"Amount must be a number. Got {type(amount).__name__}: {amount} instead")
        if amount <= 0:
            raise InvalidExpenseDataError(f"Amount must be positive. Got {amount} instead")
        return amount

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def amount(self) -> float:
        return self._amount
    
    def correct_amount(self, new_amount: float) -> None:
        validated_amount = self._normalize_amount(new_amount)
        if validated_amount == self.amount:
            return
        self._amount = validated_amount
    
    @property
    def category(self) -> str:
        return self._category
    
    def recategorize(self, new_category: str) -> None:
        if not new_category:
            raise InvalidCategoryError("Category must be a non-empty string")
        if new_category == self.category:
            return
        self._category = new_category

    @property
    def description(self) -> str:
        return self._description
    
    def correct_description(self, new_description: str) -> None:
        if not new_description:
            raise InvalidExpenseDescriptionError("Description must be a non-empty string")
        if new_description == self.description:
            return
        self._description = new_description

    @property
    def date(self) -> Date:
        return self._date
    
    def correct_date(self, new_date: Date) -> None:
        if not isinstance(new_date, Date):
            raise InvalidDateError(f"Date must be a datetime Date. Got {type(new_date).__name__}: {new_date} instead")
        if new_date == self.date:
            return
        self._date = new_date

    def to_csv_row(self) -> list:
        """Return expense as a list for CSV writing"""
        return [
        self.id,
        self.amount,
        self.category,
        self.description,
        self.date.isoformat()
        ]
    
    @classmethod
    def from_csv_row(cls, row: list) -> "Expense":
        """Returns Expense object from CSV row"""
        expense_id = int(row[0])
        amount = float(row[1])
        category = row[2]
        description = row[3]
        date = Date.fromisoformat(row[4])

        return cls(expense_id, amount, category, description, date)