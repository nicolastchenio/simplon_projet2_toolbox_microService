"""Application entry point.

This script reads a CSV file describing mathematical operations,
executes them using functions from the business logic module,
and prints the results.
"""

import os

import pandas as pd

from .maths.mon_module import add, print_data, square, sub

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "moncsv.csv")


def execute_operations(df: pd.DataFrame) -> None:
    """Execute mathematical operations described in a DataFrame.

    The DataFrame must contain the following columns:
    - operation: name of the operation ("add", "sub", "square")
    - a: first operand
    - b: second operand (optional for square)

    Args:
        df (pd.DataFrame): DataFrame containing the operations to execute.

    """
    for _, row in df.iterrows():
        operation = row["operation"]
        a = row["a"]
        b = row["b"]

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
    """Run the application workflow.

    Steps:
        1. Load the CSV file containing operations.
        2. Display the dataset.
        3. Execute the operations defined in the file.
    """
    df = pd.read_csv(CSV_FILE_PATH)

    print("Loaded dataset:")
    print_data(df)

    print("\nExecuting operations:\n")
    execute_operations(df)


if __name__ == "__main__":
    main()
