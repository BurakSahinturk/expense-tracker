# Expense Tracker

A command-line expense tracking application with an interactive text-based UI.

## Features

- Add expenses with amount, category, and description
- View all expenses in a formatted table
- Delete expenses with confirmation
- View spending summary by category
- Persistent storage using CSV
- Interactive TUI with arrow-key navigation

## Dependencies:

- inquirer

## Usage

Run the application:

```
python main.py
```

Navigate using arrow keys, Enter to select.

## Project Structure

- `expense.py` - Expense domain model
- `expense_manager.py` - Business logic
- `storage.py` - CSV file operations
- `cli_input.py` - User input handling (TUI)
- `cli_view.py` - Display formatting
- `main.py` - Main controller
- `exceptions.py` - Custom exceptions

## Categories

- Groceries
- Transportation
- Utilities
- Personal Care
- Savings
- Entertainment
