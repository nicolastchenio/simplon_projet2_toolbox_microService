"""Test suite for mathematical operations and DataFrame utilities."""

import pandas as pd
import pytest

from app.modules.mon_module import add, print_data, square, sub


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 5, 8),
        (10, 2, 12),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
def test_add(a, b, expected):
    """Test the add function with multiple input values."""
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 3),
        (10, 5, 5),
        (0, 2, -2),
        (-5, -5, 0),
    ],
)
def test_sub(a, b, expected):
    """Test the sub function with multiple input values."""
    assert sub(a, b) == expected


@pytest.mark.parametrize(
    "a, expected",
    [
        (2, 4),
        (5, 25),
        (0, 0),
        (-3, 9),
    ],
)
def test_square(a, expected):
    """Test the square function."""
    assert square(a) == expected


@pytest.fixture
def sample_dataframe():
    """Provide a temporary DataFrame for testing."""
    return pd.DataFrame(
        {
            "operation": ["add", "sub", "square"],
            "a": [1, 5, 3],
            "b": [2, 1, None],
        }
    )


def test_print_data(sample_dataframe):
    """Test that print_data returns the correct number of rows."""
    rows = print_data(sample_dataframe)
    assert rows == 3
