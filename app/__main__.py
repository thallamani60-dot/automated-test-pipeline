"""Run a short demonstration of the example application."""

from app.utils import (
    calculate_average,
    celsius_to_fahrenheit,
    count_words,
    is_palindrome,
    normalize_whitespace,
    safe_divide,
)


def main() -> None:
    """Print sample results from the utility functions."""
    print("Python CI sample application")
    print(f"Normalized text: {normalize_whitespace('  hello   CI  ')}")
    print(f"Word count: {count_words('GitHub Actions runs these tests')}")
    print(f"Palindrome: {is_palindrome('A man, a plan, a canal: Panama')}")
    print(f"Average: {calculate_average([10, 20, 30]):.1f}")
    print(f"Division: {safe_divide(10, 2):.1f}")
    print(f"20 C in Fahrenheit: {celsius_to_fahrenheit(20):.1f} F")


if __name__ == "__main__":
    main()
