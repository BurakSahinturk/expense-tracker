from expense import Expense
import csv
import os
from exceptions import CorruptedDataError

def save_expenses(filepath: str, expenses: list[Expense], next_id: int) -> None:
    """Save list of expenses to CSV file"""
    try:
        with open(filepath, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["next ID:", next_id])
            csv_writer.writerow(["id", "amount", "category", "description", "date"])
            csv_writer.writerows([expense.to_csv_row() for expense in expenses])
    except OSError as e:
        raise OSError(f"Failed to save expenses: {e}") from e

def load_expenses(filepath: str) -> tuple[list[Expense], int]:
    """Load expenses from CSV file
    Returns:
        tuple: (list of Expense objects, next_id)
    """
    if not os.path.exists(filepath): # If file does not exist
        return ([], 1)
    if os.path.getsize(filepath) < 40: # If file is empty
        return ([], 1)
    try:
        with open(filepath, "r", newline="") as file:
            csv_reader = csv.reader(file)
            next_id_row = next(csv_reader)  # Read first row - next ID row
            try:
                next_id = int(next_id_row[1])
            except (ValueError, IndexError) as e:
                raise CorruptedDataError(f"Corrupted CSV: Invalid next_id format") from e
            next(csv_reader)  # Read and skip the second row - header
            expenses = []
            for row in csv_reader:
                try:
                    expenses.append(Expense.from_csv_row(row))
                except Exception as e:
                    print(f"Warning: Skipping corrupted row: {row} - {e}") #Error handling to be corrected later.
            return expenses, next_id
    except PermissionError as e:
        raise PermissionError(f"No permission to read {filepath}") from e
    except Exception as e:
        raise OSError(f"Failed to load expenses from {filepath}: {e}") from e