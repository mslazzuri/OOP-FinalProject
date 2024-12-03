import unittest
from unittest.mock import Mock, patch
from tkinter import Tk as tk, StringVar
from calculator import (
    CalculatorBase,
    ConversionContext,
    ConversionStrategy,
    MilesToKmStrategy,
    KmToMilesStrategy,
    CelsiusToFahrenheitStrategy,
    FahrenheitToCelsiusStrategy,
    InchesToCentimetersStrategy,
    CentimetersToInchesStrategy,
    MinutesToSecondsStrategy,
    SecondsToMinutesStrategy,
    CalculatorMode,
    StandardMode,
    ConvertMode,
    AppMediator,
    Display,
    ButtonManager
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


class TestConversionStrategy(unittest.TestCase):
    def test_convert_not_implemented(self):
        strategy = ConversionStrategy()
        with self.assertRaises(NotImplementedError):
            strategy.convert(5.6)


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

    @given(st.floats(min_value=-1e6, max_value=1e6))
    def test_in_to_cm(self, value):
        """Property-based test for kilometers to miles."""
        strategy = InchesToCentimetersStrategy()
        result = strategy.convert(value)
        self.assertAlmostEqual(result, value * 2.54)

    @given(st.floats(min_value=-1e6, max_value=1e6))
    def test_cm_to_in(self, value):
        """Property-based test for kilometers to miles."""
        strategy = CentimetersToInchesStrategy()
        result = strategy.convert(value)
        self.assertAlmostEqual(result, value * 0.3937)

    @given(st.floats(min_value=-1e6, max_value=1e6))
    def test_min_to_sec(self, value):
        """Property-based test for kilometers to miles."""
        strategy = MinutesToSecondsStrategy()
        result = strategy.convert(value)
        self.assertAlmostEqual(result, value * 60)

    @given(st.floats(min_value=-1e6, max_value=1e6))
    def test_sec_to_min(self, value):
        """Property-based test for kilometers to miles."""
        strategy = SecondsToMinutesStrategy()
        result = strategy.convert(value)
        self.assertAlmostEqual(result, value / 60)


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


class TestCalculatorMode(unittest.TestCase):
    def test_create_buttons_not_implemented(self):
        mode = CalculatorMode()
        with self.assertRaises(NotImplementedError):
            mode.create_buttons()


class TestAppMediator(unittest.TestCase):
    """Tests for the App Mediator class."""
    def setUp(self):
        """Set up the AppMediator with a real Tk instance."""
        self.master = tk()  # Create a real Tk instance
        self.mediator = AppMediator(self.master)

        # Replace display and button_manager with mocks
        self.mediator.display = Mock()
        self.mediator.button_manager = Mock()

    def tearDown(self):
        self.master.destroy()

    def test_set_standard_mode(self):
        self.mediator.set_standard_mode()
        self.assertIsInstance(self.mediator.mode, StandardMode)
        self.assertEqual(self.mediator.button_manager.update_buttons.call_count, 1)

    def test_set_convert_mode(self):
        self.mediator.set_convert_mode()
        self.assertIsInstance(self.mediator.mode, ConvertMode)
        self.assertEqual(self.mediator.button_manager.update_buttons.call_count, 1)

    def test_handle_clear(self):
        with patch.object(self.mediator.calculator, 'clear') as mock_clear:
            self.mediator.handle_clear()
            mock_clear.assert_called_once()
            self.mediator.display.update_display.assert_called_once_with("")

    def test_handle_equal(self):
        with patch.object(self.mediator.calculator, 'solve', return_value=42):
            self.mediator.handle_equal()
            self.assertEqual(self.mediator.calculator.solve.call_count, 1)
            self.mediator.display.update_display.assert_called_once_with(42)

    def test_handle_append(self):
        with patch.object(self.mediator.calculator, 'append') as mock_append:
            self.mediator.handle_append("5")
            mock_append.assert_called_once_with("5")
            self.mediator.display.update_display.assert_called_once_with(self.mediator.calculator.entry_value)

    def test_handle_conversion(self):
        self.mediator.calculator.entry_value = "10"
        with patch.object(self.mediator.conversion_context, 'set_strategy') as mock_set_strategy, \
             patch.object(self.mediator.conversion_context, 'execute_conversion', return_value=16.0934) as mock_execute_conversion:
            self.mediator.handle_conversion("Mi to Km")
            self.assertEqual(mock_set_strategy.call_count, 1)
            self.assertEqual(mock_execute_conversion.call_count, 1)
            self.mediator.display.update_display.assert_called_once_with(16.0934)

    def test_handle_conversion_invalid_value(self):
        self.mediator.calculator.entry_value = "invalid"
        self.mediator.handle_conversion("Mi to Km")
        self.mediator.display.update_display.assert_called_once_with("Error")


class TestDisplay(unittest.TestCase):
    """Tests for Display class methods that haven't been covered"""

    def setUp(self):
        self.master = tk()
        self.mock_mediator = Mock()
        self.display = Display(self.master, self.mock_mediator)
        self.display.equation = StringVar()

    @given(st.floats(allow_infinity=False, allow_nan=False))
    def test_update_display_with_float(self, value):
        self.display.update_display(value)
        self.assertEqual(self.display.equation.get(), f"{value:.3f}")

    @given(st.integers())
    def test_update_display_with_int(self, value):
        self.display.update_display(value)
        self.assertEqual(self.display.equation.get(), f"{value:.3f}")

    @given(st.text())
    def test_update_display_with_str(self, value):
        self.display.update_display(value)
        self.assertEqual(self.display.equation.get(), value)

    def test_update_display_with_edge_case_values(self):
        self.display.update_display("")  # Empty string
        self.assertEqual(self.display.equation.get(), "")
        
        self.display.update_display(0)  # Zero
        self.assertEqual(self.display.equation.get(), "0.000")


class TestButtonManager(unittest.TestCase):
    """Tests for the ButtonManager class."""

    def setUp(self):
        self.master = tk()
        self.mock_mediator = Mock()
        self.mock_mediator.mode = Mock()
        self.mock_mediator.mode.create_buttons.return_value = [
            ("C", 0, 0),
            ("=", 1, 1),
            ("5", 2, 2),
            ("Mi to Km", 3, 3),
        ]
        self.button_manager = ButtonManager(self.master, self.mock_mediator)

    def tearDown(self):
        self.master.destroy()
        
    def test_update_buttons_clears_existing_widgets(self):
        """Ensure update_buttons destroys all existing widgets."""
        # Mock existing widgets in the button_frame
        mock_widget1 = Mock()
        mock_widget2 = Mock()
        self.button_manager.button_frame.winfo_children = Mock(
            return_value=[mock_widget1, mock_widget2]
        )

        # Call update_buttons
        self.button_manager.update_buttons()

        # Ensure destroy was called for each widget
        mock_widget1.destroy.assert_called_once()
        mock_widget2.destroy.assert_called_once()

    @patch("calculator.Button")
    def test_create_standard_button_handles_clear(self, mock_button):
        """Test 'C' button calls mediator's handle_clear."""
        with patch.object(self.mock_mediator, "handle_clear") as mock_handle_clear:
            self.button_manager.create_standard_button("C", 0, 0)
            mock_button.assert_called_once_with(
                self.button_manager.button_frame, width=7, height=4, text="C",
                relief='flat', bg='#7A8450', activebackground='#AEBD93', fg='white',
                bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
                command=unittest.mock.ANY
            )
            # Simulate button click
            command = mock_button.call_args[1]["command"]
            command()  # Execute the button command
            mock_handle_clear.assert_called_once()

    @patch("calculator.Button")
    def test_create_standard_button_handles_equal(self, mock_button):
        """Test '=' button calls mediator's handle_equal."""
        with patch.object(self.mock_mediator, "handle_equal") as mock_handle_equal:
            self.button_manager.create_standard_button("=", 1, 1)
            mock_button.assert_called_once_with(
                self.button_manager.button_frame, width=7, height=4, text="=",
                relief='flat', bg='#7A8450', activebackground='#AEBD93', fg='white',
                bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
                command=unittest.mock.ANY
            )
            # Simulate button click
            command = mock_button.call_args[1]["command"]
            command()  # Execute the button command
            mock_handle_equal.assert_called_once()

    @patch("calculator.Button")
    def test_create_standard_button_handles_append(self, mock_button):
        """Test a number button calls mediator's handle_append."""
        with patch.object(self.mock_mediator, "handle_append") as mock_handle_append:
            self.button_manager.create_standard_button("5", 2, 2)
            mock_button.assert_called_once_with(
                self.button_manager.button_frame, width=7, height=4, text="5",
                relief='flat', bg='#7A8450', activebackground='#AEBD93', fg='white',
                bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
                command=unittest.mock.ANY
            )
            # Simulate button click
            command = mock_button.call_args[1]["command"]
            command()  # Execute the button command
            mock_handle_append.assert_called_once_with("5")

    @patch("calculator.Button")
    def test_create_conversion_button_handles_conversion(self, mock_button):
        """Test conversion button calls mediator's handle_conversion."""
        with patch.object(self.mock_mediator, "handle_conversion") as mock_handle_conversion:
            self.button_manager.create_conversion_button("Mi to Km", 3, 3)
            mock_button.assert_called_once_with(
                self.button_manager.button_frame, width=7, height=4, text="Mi to Km",
                relief='flat', bg='white', activebackground='white', fg='black',
                bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
                command=unittest.mock.ANY
            )
            # Simulate button click
            command = mock_button.call_args[1]["command"]
            command()  # Execute the button command
            mock_handle_conversion.assert_called_once_with("Mi to Km")



if __name__ == "__main__":
    unittest.main()
