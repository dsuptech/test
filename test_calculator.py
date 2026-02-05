"""
Tests for the Calculator Module
"""

import unittest
from calculator import Calculator, calculate


class TestCalculator(unittest.TestCase):
    """Test cases for the Calculator class."""

    def setUp(self):
        """Set up a calculator instance for each test."""
        self.calc = Calculator()

    # Test addition
    def test_add_positive_numbers(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(self.calc.add(-2, -3), -5)

    def test_add_mixed_numbers(self):
        self.assertEqual(self.calc.add(-2, 3), 1)

    def test_add_floats(self):
        self.assertAlmostEqual(self.calc.add(2.5, 3.5), 6.0)

    # Test subtraction
    def test_subtract_positive_numbers(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_subtract_negative_numbers(self):
        self.assertEqual(self.calc.subtract(-5, -3), -2)

    def test_subtract_mixed_numbers(self):
        self.assertEqual(self.calc.subtract(-5, 3), -8)

    def test_subtract_floats(self):
        self.assertAlmostEqual(self.calc.subtract(5.5, 2.5), 3.0)

    # Test multiplication
    def test_multiply_positive_numbers(self):
        self.assertEqual(self.calc.multiply(4, 5), 20)

    def test_multiply_negative_numbers(self):
        self.assertEqual(self.calc.multiply(-4, -5), 20)

    def test_multiply_mixed_numbers(self):
        self.assertEqual(self.calc.multiply(-4, 5), -20)

    def test_multiply_by_zero(self):
        self.assertEqual(self.calc.multiply(5, 0), 0)

    def test_multiply_floats(self):
        self.assertAlmostEqual(self.calc.multiply(2.5, 4), 10.0)

    # Test division
    def test_divide_positive_numbers(self):
        self.assertEqual(self.calc.divide(20, 4), 5)

    def test_divide_negative_numbers(self):
        self.assertEqual(self.calc.divide(-20, -4), 5)

    def test_divide_mixed_numbers(self):
        self.assertEqual(self.calc.divide(-20, 4), -5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")

    def test_divide_floats(self):
        self.assertAlmostEqual(self.calc.divide(7.5, 2.5), 3.0)

    # Test power
    def test_power_positive(self):
        self.assertEqual(self.calc.power(2, 3), 8)

    def test_power_zero_exponent(self):
        self.assertEqual(self.calc.power(5, 0), 1)

    def test_power_negative_exponent(self):
        self.assertAlmostEqual(self.calc.power(2, -1), 0.5)

    def test_power_float(self):
        self.assertAlmostEqual(self.calc.power(4, 0.5), 2.0)

    # Test modulo
    def test_modulo_positive(self):
        self.assertEqual(self.calc.modulo(17, 5), 2)

    def test_modulo_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calc.modulo(10, 0)
        self.assertEqual(str(context.exception), "Cannot calculate modulo with zero divisor")

    # Test square root
    def test_square_root_positive(self):
        self.assertEqual(self.calc.square_root(16), 4)

    def test_square_root_zero(self):
        self.assertEqual(self.calc.square_root(0), 0)

    def test_square_root_negative(self):
        with self.assertRaises(ValueError) as context:
            self.calc.square_root(-4)
        self.assertEqual(str(context.exception), "Cannot calculate square root of a negative number")

    def test_square_root_non_perfect(self):
        self.assertAlmostEqual(self.calc.square_root(2), 1.4142135623730951)

    # Test memory functions
    def test_memory_initial_value(self):
        self.assertEqual(self.calc.recall(), 0)

    def test_memory_store_and_recall(self):
        self.calc.store(42)
        self.assertEqual(self.calc.recall(), 42)

    def test_memory_clear(self):
        self.calc.store(42)
        self.calc.clear_memory()
        self.assertEqual(self.calc.recall(), 0)


class TestCalculateFunction(unittest.TestCase):
    """Test cases for the calculate function."""

    def test_calculate_addition(self):
        self.assertEqual(calculate("5 + 3"), 8)

    def test_calculate_subtraction(self):
        self.assertEqual(calculate("10 - 4"), 6)

    def test_calculate_multiplication(self):
        self.assertEqual(calculate("6 * 7"), 42)

    def test_calculate_division(self):
        self.assertEqual(calculate("20 / 4"), 5.0)

    def test_calculate_power(self):
        self.assertEqual(calculate("2 ^ 3"), 8)

    def test_calculate_modulo(self):
        self.assertEqual(calculate("17 % 5"), 2)

    def test_calculate_single_number(self):
        self.assertEqual(calculate("42"), 42)

    def test_calculate_float(self):
        self.assertAlmostEqual(calculate("3.14"), 3.14)

    def test_calculate_invalid_expression(self):
        with self.assertRaises(ValueError):
            calculate("invalid")


if __name__ == "__main__":
    unittest.main()
