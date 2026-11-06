"""Small utility functions used to demonstrate Python testing and CI."""

from collections.abc import Sequence


def normalize_whitespace(text: str) -> str:
    """Trim text and replace each run of whitespace with one space."""
    return " ".join(text.split())


def count_words(text: str) -> int:
    """Count whitespace-separated words in *text*."""
    return len(normalize_whitespace(text).split())


def is_palindrome(text: str) -> bool:
    """Return whether alphanumeric characters read the same in both directions.

    Case and punctuation are ignored. Text without alphanumeric characters is
    considered a palindrome because its normalized form is empty.
    """
    normalized = "".join(
        character.casefold() for character in text if character.isalnum()
    )
    return normalized == normalized[::-1]


def calculate_average(values: Sequence[float]) -> float:
    """Return the arithmetic mean of *values*.

    Raises:
        ValueError: If *values* is empty.
    """
    if not values:
        raise ValueError("Cannot calculate the average of an empty sequence.")
    return sum(values) / len(values)


def safe_divide(numerator: float, denominator: float) -> float:
    """Divide two numbers, raising a clear error when the denominator is zero."""
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return numerator / denominator


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature in degrees Celsius to degrees Fahrenheit."""
    return (celsius * 9 / 5) + 32
