import unittest
from pkg.calculator import Calculator

calculator = Calculator()

class TestCalculator(unittest.TestCase):

    def test_add(self):
        # Test addition
        self.assertEqual(calculator.evaluate("2+2"), 4)
        self.assertEqual(calculator.evaluate("2 + 2"), 4)

    def test_subtract(self):
        # Test subtraction
        self.assertEqual(calculator.evaluate("5-3"), 2)
        self.assertEqual(calculator.evaluate("5 - 3"), 2)

    def test_multiply(self):
        # Test multiplication
        self.assertEqual(calculator.evaluate("2*3"), 6)
        self.assertEqual(calculator.evaluate("2 * 3"), 6)

    def test_divide(self):
        # Test division
        self.assertEqual(calculator.evaluate("6/3"), 2)
        self.assertEqual(calculator.evaluate("6 / 3"), 2)

    def test_divide_by_zero(self):
        # Test division by zero
        with self.assertRaises(ZeroDivisionError):
            calculator.evaluate("6/0")

    def test_complex_expression(self):
        # Test a more complex expression
        self.assertEqual(calculator.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(calculator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(calculator.evaluate("(10 - 2) / 4"), 2)

    def test_invalid_expression(self):
        # Test an invalid expression
        with self.assertRaises(ValueError):
            calculator.evaluate("2 + ")


if __name__ == '__main__':
    unittest.main()