"""
Application entry point using SQLite database.

This script reads mathematical operations stored in the database,
executes them using functions from the business logic module,
and prints the results.

The database is accessed via SQLAlchemy models and sessions.
"""

from typing import List

from sqlalchemy.orm import Session

from .modules.mon_module import add, sub, square, print_data
from .modules.crud import get_all_data
from .modules.connect import get_db


def execute_operations(operations: List[dict]) -> None:
    """
    Execute mathematical operations provided as a list of dictionaries.

    Each dictionary must contain:
        - 'operation': str, one of "add", "sub", "square"
        - 'a': float, first operand
        - 'b': float | None, second operand (optional for square)

    Args:
        operations (List[dict]): List of operations to execute.
    """
    for op in operations:
        operation = op.get("operation")
        a = op.get("a")
        b = op.get("b")

        if operation == "add":
            result = add(a, b)
        elif operation == "sub":
            result = sub(a, b)
        elif operation == "square":
            result = square(a)
        else:
            print(f"Unknown operation: {operation}")
            continue

        print(f"{operation}({a}, {b}) = {result}")


def main() -> None:
    """
    Main workflow of the application.

    Steps:
        1. Connect to the SQLite database using SQLAlchemy.
        2. Retrieve all operations stored in the 'operations' table.
        3. Display the retrieved dataset.
        4. Execute each operation using the business logic functions.
    """
    # Obtenir une session de DB
    db: Session = next(get_db())

    # Récupérer toutes les opérations
    operations = get_all_data(db)

    print("Loaded dataset from database:")
    print_data(operations)

    print("\nExecuting operations:\n")
    execute_operations(operations)


if __name__ == "__main__":
    main()