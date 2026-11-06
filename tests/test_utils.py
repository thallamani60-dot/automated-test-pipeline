"""Unit tests for the sample utility functions."""

import pytest

from app.utils import (
    calculate_average,
    celsius_to_fahrenheit,
    count_words,
    is_palindrome,
    normalize_whitespace,
    safe_divide,
)


def test_normalize_whitespace_trims_and_collapses_spaces() -> None:
    assert normalize_whitespace("  hello\t world  ") == "hello world"


def test_count_words_returns_zero_for_empty_text() -> None:
    assert count_words(" \n\t ") == 0


def test_count_words_counts_words_with_mixed_whitespace() -> None:
    assert count_words("one\ntwo   three") == 3


def test_is_palindrome_ignores_case_and_punctuation() -> None:
    assert is_palindrome("A man, a plan, a canal: Panama") is True


def test_is_palindrome_returns_false_for_different_text() -> None:
    assert is_palindrome("GitHub Actions") is False


def test_is_palindrome_treats_no_alphanumeric_characters_as_empty() -> None:
    assert is_palindrome("!!!") is True


def test_calculate_average_returns_mean_for_positive_and_negative_values() -> None:
    assert calculate_average([2, -2, 6]) == pytest.approx(2.0)


def test_calculate_average_rejects_an_empty_sequence() -> None:
    with pytest.raises(ValueError, match="empty sequence"):
        calculate_average([])


def test_safe_divide_returns_quotient() -> None:
    assert safe_divide(9, 3) == 3


def test_safe_divide_rejects_zero_denominator() -> None:
    with pytest.raises(ZeroDivisionError, match="zero"):
        safe_divide(9, 0)


def test_celsius_to_fahrenheit_converts_freezing_point() -> None:
    assert celsius_to_fahrenheit(0) == 32


def test_celsius_to_fahrenheit_handles_negative_forty_edge_case() -> None:
    assert celsius_to_fahrenheit(-40) == -40
