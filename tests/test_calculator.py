"""
Tests for the calculator module.
"""
import pytest
from calculator.calculator import add


class TestCalculator:
    """Test suite for calculator functions."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        result = add(2, 3)
        assert result == 5

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        result = add(-2, -3)
        assert result == -5

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        result = add(5, -3)
        assert result == 2

    def test_add_zero(self):
        """Test adding zero to a number."""
        result = add(5, 0)
        assert result == 5

    def test_add_floats(self):
        """Test adding floating point numbers."""
        result = add(2.5, 3.7)
        assert result == pytest.approx(6.2)
