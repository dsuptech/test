import unittest

from calculator import CalculatorError, add, divide, evaluate, multiply, power, subtract


class TestCalculator(unittest.TestCase):
    def test_basic_operations(self) -> None:
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(multiply(3, 7), 21)
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(divide(8, 2), 4)

    def test_expression_eval(self) -> None:
        self.assertEqual(evaluate("2 + 3 * 4"), 14)
        self.assertAlmostEqual(evaluate("10 / 4"), 2.5)
        self.assertEqual(evaluate("(1 + 2) * (3 + 4)"), 21)

    def test_rejects_unsafe_input(self) -> None:
        with self.assertRaises(CalculatorError):
            evaluate("__import__('os').system('echo hacked')")

    def test_invalid_syntax(self) -> None:
        with self.assertRaises(CalculatorError):
            evaluate("2 + * 3")


if __name__ == "__main__":
    unittest.main()
