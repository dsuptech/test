#!/usr/bin/env python3
"""
Unit tests for the Calculator class.
"""

import unittest
import math
from calculator import Calculator


class TestCalculatorBasicOperations(unittest.TestCase):
    """Test basic arithmetic operations."""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0.1, 0.2), 0.30000000000000004)
        self.assertEqual(self.calc.add(-5, -3), -8)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(3, 5), -2)
        self.assertEqual(self.calc.subtract(0, 0), 0)
        self.assertEqual(self.calc.subtract(-5, -3), -2)
    
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 5), 20)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)
        self.assertEqual(self.calc.multiply(-2, -3), 6)
    
    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        self.assertEqual(self.calc.divide(-6, 2), -3)
        self.assertEqual(self.calc.divide(0, 5), 0)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")


class TestCalculatorAdvancedOperations(unittest.TestCase):
    """Test advanced mathematical operations."""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(2, -1), 0.5)
        self.assertEqual(self.calc.power(4, 0.5), 2)
    
    def test_square_root(self):
        self.assertEqual(self.calc.square_root(4), 2)
        self.assertEqual(self.calc.square_root(9), 3)
        self.assertEqual(self.calc.square_root(0), 0)
        self.assertAlmostEqual(self.calc.square_root(2), math.sqrt(2))
    
    def test_square_root_negative(self):
        with self.assertRaises(ValueError) as context:
            self.calc.square_root(-1)
        self.assertEqual(str(context.exception), "Cannot calculate square root of negative number")
    
    def test_modulo(self):
        self.assertEqual(self.calc.modulo(10, 3), 1)
        self.assertEqual(self.calc.modulo(15, 5), 0)
        self.assertEqual(self.calc.modulo(7, 2), 1)
    
    def test_modulo_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calc.modulo(10, 0)
        self.assertEqual(str(context.exception), "Cannot perform modulo by zero")
    
    def test_absolute(self):
        self.assertEqual(self.calc.absolute(5), 5)
        self.assertEqual(self.calc.absolute(-5), 5)
        self.assertEqual(self.calc.absolute(0), 0)
    
    def test_factorial(self):
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(1), 1)
        self.assertEqual(self.calc.factorial(5), 120)
        self.assertEqual(self.calc.factorial(10), 3628800)
    
    def test_factorial_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)
        with self.assertRaises(ValueError):
            self.calc.factorial(3.5)
    
    def test_logarithm(self):
        self.assertAlmostEqual(self.calc.logarithm(math.e), 1)
        self.assertAlmostEqual(self.calc.logarithm(10, 10), 1)
        self.assertAlmostEqual(self.calc.logarithm(8, 2), 3)
    
    def test_logarithm_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.logarithm(0)
        with self.assertRaises(ValueError):
            self.calc.logarithm(-5)
        with self.assertRaises(ValueError):
            self.calc.logarithm(10, 1)


class TestCalculatorTrigonometry(unittest.TestCase):
    """Test trigonometric functions."""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_sin(self):
        self.assertAlmostEqual(self.calc.sin(0), 0)
        self.assertAlmostEqual(self.calc.sin(math.pi / 2), 1)
        self.assertAlmostEqual(self.calc.sin(90, degrees=True), 1)
    
    def test_cos(self):
        self.assertAlmostEqual(self.calc.cos(0), 1)
        self.assertAlmostEqual(self.calc.cos(math.pi), -1)
        self.assertAlmostEqual(self.calc.cos(180, degrees=True), -1)
    
    def test_tan(self):
        self.assertAlmostEqual(self.calc.tan(0), 0)
        self.assertAlmostEqual(self.calc.tan(math.pi / 4), 1)
        self.assertAlmostEqual(self.calc.tan(45, degrees=True), 1)


class TestCalculatorHistory(unittest.TestCase):
    """Test history functionality."""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_history_recording(self):
        self.calc.add(2, 3)
        self.calc.multiply(4, 5)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], "2 + 3 = 5")
        self.assertEqual(history[1], "4 * 5 = 20")
    
    def test_last_result(self):
        self.calc.add(2, 3)
        self.assertEqual(self.calc.get_last_result(), 5)
        self.calc.multiply(4, 5)
        self.assertEqual(self.calc.get_last_result(), 20)
    
    def test_clear_history(self):
        self.calc.add(2, 3)
        self.calc.multiply(4, 5)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)
        self.assertEqual(self.calc.get_last_result(), 0)
    
    def test_history_immutability(self):
        self.calc.add(1, 1)
        history = self.calc.get_history()
        history.append("fake entry")
        self.assertEqual(len(self.calc.get_history()), 1)


class TestCalculatorEdgeCases(unittest.TestCase):
    """Test edge cases and special values."""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_large_numbers(self):
        large = 10 ** 100
        self.assertEqual(self.calc.add(large, large), 2 * large)
        self.assertEqual(self.calc.multiply(large, 2), 2 * large)
    
    def test_very_small_numbers(self):
        small = 1e-100
        result = self.calc.add(small, small)
        self.assertAlmostEqual(result, 2e-100)
    
    def test_float_precision(self):
        # Known floating point precision issue
        result = self.calc.add(0.1, 0.2)
        self.assertAlmostEqual(result, 0.3, places=10)


if __name__ == "__main__":
    unittest.main()
