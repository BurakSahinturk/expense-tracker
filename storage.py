# Persistence Layer
from expense import Expense, ExpenseDraft
import sqlite3
from datetime import date as Date

def create_table(filepath):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_expense(filepath: str, expense: ExpenseDraft) -> Expense:
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO expenses(amount, category, description, date)
            VALUES(?, ?, ?, ?)
        ''',
        (expense.amount, expense.category, expense.description, expense.date )
        )
        new_id = cursor.lastrowid
        conn.commit()
        if new_id is None:
            raise RuntimeError(f"Failed to insert expense")
        return Expense(new_id, expense.amount, expense.category, expense.description, expense.date)
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to insert expense: {e}") from e
    finally:
        conn.close()

def load_expenses(filepath: str) -> list[Expense]:
    conn = sqlite3.connect(filepath)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM expenses')
        rows = cursor.fetchall()
        expense_list = []
        for row in rows:
            expense_list.append(Expense(
                row["id"],
                row["amount"],
                row["category"],
                row["description"],
                Date.fromisoformat(row["date"])
            ))
        return expense_list

    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to load from database: {e}") from e
    finally:
        conn.close()

def delete_expense(filepath, expense_id):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()

def update_expense_amount(filepath, expense_id, new_value):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute('UPDATE expenses SET amount = ? WHERE id = ?', (new_value, expense_id))
    conn.commit()
    conn.close()

def update_expense_category(filepath, expense_id, new_value):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute('UPDATE expenses SET category = ? WHERE id = ?', (new_value, expense_id))
    conn.commit()
    conn.close()

def update_expense_description(filepath, expense_id, new_value):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute('UPDATE expenses SET description = ? WHERE id = ?', (new_value, expense_id))
    conn.commit()
    conn.close()

def update_expense_date(filepath, expense_id, new_value):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute('UPDATE expenses SET date = ? WHERE id = ?',(new_value, expense_id))
    conn.commit()
    conn.close()