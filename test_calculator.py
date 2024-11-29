import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from calculator import (
    CalculatorBase,
    ConversionContext,
    MilesToKmStrategy,
    KmToMilesStrategy,
    CelsiusToFahrenheitStrategy,
    FahrenheitToCelsiusStrategy,
    StandardMode,
    ConvertMode,
)
from hypothesis import given, strategies as st


class TestCalculatorBase(unittest.TestCase):
    """Tests for the CalculatorBase class."""

    def setUp(self) -> None:
        self.calculator = CalculatorBase()

    def test_append_value(self):
        self.calculator.append("5")
        self.assertEqual(self.calculator.entry_value, "5")

    def test_clear_entry(self):
        self.calculator.append("123")
        self.calculator.clear()
        self.assertEqual(self.calculator.entry_value, "")

    def test_solve_valid_expression(self):
        self.calculator.append("2+2")
        result = self.calculator.solve()
        self.assertEqual(result, 4)

    def test_solve_invalid_expression(self):
        self.calculator.append("5/0")
        result = self.calculator.solve()
        self.assertEqual(result, "Error")

    def test_solve_empty_expression(self):
        result = self.calculator.solve()
        self.assertEqual(result, "Error")

    @given(st.text())
    def test_solve_random_expressions(self, expression):
        """Property-based test to ensure no crashes on arbitrary input."""
        self.calculator.entry_value = expression
        result = self.calculator.solve()
        self.assertTrue(isinstance(result, (str, int, float)))


class TestConversionStrategies(unittest.TestCase):
    """Tests for conversion strategies."""

    def test_miles_to_km(self):
        strategy = MilesToKmStrategy()
        self.assertAlmostEqual(strategy.convert(1), 1.60934)
        self.assertAlmostEqual(strategy.convert(0), 0)
        self.assertAlmostEqual(strategy.convert(-1), -1.60934)

    def test_km_to_miles(self):
        strategy = KmToMilesStrategy()
        self.assertAlmostEqual(strategy.convert(1.60934), 1)
        self.assertAlmostEqual(strategy.convert(0), 0)
        self.assertAlmostEqual(strategy.convert(-1.60934), -1)

    def test_celsius_to_fahrenheit(self):
        strategy = CelsiusToFahrenheitStrategy()
        self.assertAlmostEqual(strategy.convert(0), 32)
        self.assertAlmostEqual(strategy.convert(100), 212)
        self.assertAlmostEqual(strategy.convert(-40), -40)

    def test_fahrenheit_to_celsius(self):
        strategy = FahrenheitToCelsiusStrategy()
        self.assertAlmostEqual(strategy.convert(32), 0)
        self.assertAlmostEqual(strategy.convert(212), 100)
        self.assertAlmostEqual(strategy.convert(-40), -40)

    @given(st.floats(min_value=-1e6, max_value=1e6))
    def test_property_miles_to_km(self, value):
        """Property-based test for miles to kilometers."""
        strategy = MilesToKmStrategy()
        result = strategy.convert(value)
        self.assertAlmostEqual(result, value * 1.60934)

    @given(st.floats(min_value=-1e6, max_value=1e6))
    def test_property_km_to_miles(self, value):
        """Property-based test for kilometers to miles."""
        strategy = KmToMilesStrategy()
        result = strategy.convert(value)
        self.assertAlmostEqual(result, value / 1.60934)


class TestConversionContext(unittest.TestCase):
    """Tests for the ConversionContext class."""

    def setUp(self) -> None:
        self.context = ConversionContext()

    def test_set_strategy(self):
        strategy = MilesToKmStrategy()
        self.context.set_strategy(strategy)
        self.assertEqual(self.context.strategy, strategy)

    def test_execute_conversion_with_strategy(self):
        self.context.set_strategy(MilesToKmStrategy())
        result = self.context.execute_conversion(1)
        self.assertAlmostEqual(result, 1.60934)

    def test_execute_conversion_without_strategy(self):
        with self.assertRaises(ValueError):
            self.context.execute_conversion(1)


class TestCalculatorModes(unittest.TestCase):
    """Tests for the Calculator Modes (Standard and Convert)."""

    def test_standard_mode_buttons(self):
        mode = StandardMode()
        buttons = mode.create_buttons()
        self.assertIn(('1', 3, 0), buttons)
        self.assertIn(('=', 4, 3), buttons)
        self.assertNotIn(('Mi to Km', 0, 0), buttons)

    def test_convert_mode_buttons(self):
        mode = ConvertMode()
        buttons = mode.create_buttons()
        self.assertIn(('Mi to Km', 0, 0), buttons)
        self.assertIn(('F to C', 0, 3), buttons)
        self.assertNotIn(('=', 4, 3), buttons)


if __name__ == "__main__":
    unittest.main()
