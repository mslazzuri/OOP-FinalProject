from tkinter import Tk, Entry, Button, StringVar, Frame
from typing import Optional, Union, List, Tuple


# ------------------ Base Logic ------------------

class CalculatorBase:
    """
    Handles the core mathematical operations of the calculator.

    This class contains methods to append input values, clear the entry,
    and evaluate mathematical expressions.
    """

    def __init__(self) -> None:
        """Initialize the calculator with an empty entry value."""
        self.entry_value: str = ""

    def append(self, value: Union[str, int, float]) -> None:
        """Append a value to the current entry."""
        self.entry_value += str(value)

    def clear(self) -> None:
        """Clear the current entry."""
        self.entry_value = ""

    def solve(self) -> Union[str, float]:
        """
        Evaluate the current mathematical expression.

        Returns:
            str: 'Error' if the expression is invalid.
            float: The result of the valid mathematical expression.
        """
        try:
            return float(eval(self.entry_value))
        except Exception:
            return "Error"


# ------------------ Conversion Logic ------------------

class ConversionStrategy:
    """
    Defines a common interface for all conversion strategies.
    """

    def convert(self, value: float) -> float:
        """
        Perform the conversion on the input value.

        Args:
            value (float): The value to convert.

        Returns:
            float: The converted value.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class MilesToKmStrategy(ConversionStrategy):
    """Strategy for converting miles to kilometers."""

    def convert(self, value: float) -> float:
        return value * 1.60934


class KmToMilesStrategy(ConversionStrategy):
    """Strategy for converting kilometers to miles."""

    def convert(self, value: float) -> float:
        return value / 1.60934


class CelsiusToFahrenheitStrategy(ConversionStrategy):
    """Strategy for converting Celsius to Fahrenheit."""

    def convert(self, value: float) -> float:
        return (value * 9 / 5) + 32


class FahrenheitToCelsiusStrategy(ConversionStrategy):
    """Strategy for converting Fahrenheit to Celsius."""

    def convert(self, value: float) -> float:
        return (value - 32) * 5 / 9


class InchesToCentimeters(ConversionStrategy):
    """Strategy for converting Inches to Centimeters."""

    def convert(self, value: float) -> float:
        return value * 2.54


class CentimetersToInches(ConversionStrategy):
    """Strategy for converting Centimeters to Inches."""

    def convert(self, value: float) -> float:
        return value * 0.3937


class MinutesToSecondsStrategy(ConversionStrategy):
    """Strategy for converting minutes to seconds."""

    def convert(self, value: float) -> float:
        return value * 60


class SecondsToMinutesStrategy(ConversionStrategy):
    """Strategy for converting seconds to minutes."""

    def convert(self, value: float) -> float:
        return value / 60


class ConversionContext:
    """
    Manages the current conversion strategy and executes it.

    Implements the **Strategy Pattern** by dynamically assigning
    the conversion strategy at runtime.
    """

    def __init__(self) -> None:
        self.strategy: Optional[ConversionStrategy] = None

    def set_strategy(self, strategy: ConversionStrategy) -> None:
        """
        Set the conversion strategy.

        Args:
            strategy (ConversionStrategy): The strategy to set.
        """
        self.strategy = strategy

    def execute_conversion(self, value: float) -> float:
        """
        Execute the current strategy's conversion.

        Args:
            value (float): The value to convert.

        Returns:
            float: The converted value.

        Raises:
            ValueError: If no strategy is set.
        """
        if not self.strategy:
            raise ValueError("No conversion strategy set.")
        return self.strategy.convert(value)


# ------------------ Modes for Buttons ------------------

class CalculatorMode:
    """
    Defines a common interface for calculator modes.

    Implements the **State Pattern**, where each mode (Standard, Convert)
    represents a different state with its own behavior for button creation.
    """

    def create_buttons(self) -> List[Tuple[str, int, int]]:
        """Create the button layout for the mode."""
        raise NotImplementedError("Subclasses must implement this method.")


class StandardMode(CalculatorMode):
    """Defines buttons for the standard calculator mode."""

    def create_buttons(self) -> List[Tuple[str, int, int]]:
        return [
            ('(', 0, 0), (')', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('.', 4, 2), ('=', 4, 3),
        ]


class ConvertMode(CalculatorMode):
    """Defines buttons for the conversion calculator mode."""

    def create_buttons(self) -> List[Tuple[str, int, int]]:
        return [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('C', 4, 0), ('0', 4, 1), ('.', 4, 2),
            ('Mi to Km', 0, 0), ('Km to Mi', 0, 1),
            ('C to F', 0, 2), ('F to C', 0, 3),
            ('In to Cm', 1, 3), ('Cm to In', 2, 3),
            ('Min to Sec', 3, 3), ('Sec to Min', 4, 3)
        ]


# ------------------ Mediator ------------------

class AppMediator:
    """
    Central mediator for managing the application state and communication.

    Implements the **Mediator Pattern** to reduce coupling and circular
    dependency between components.
    """

    def __init__(self, master: Tk) -> None:
        self.calculator = CalculatorBase()
        self.conversion_context = ConversionContext()
        self.mode: CalculatorMode = StandardMode()
        self.display = Display(master, self)
        self.button_manager = ButtonManager(master, self)

    def set_standard_mode(self) -> None:
        """Set the calculator to Standard mode."""
        self.mode = StandardMode()
        self.button_manager.update_buttons()

    def set_convert_mode(self) -> None:
        """Set the calculator to Convert mode."""
        self.mode = ConvertMode()
        self.button_manager.update_buttons()

    def handle_clear(self) -> None:
        """Clear the calculator display."""
        self.calculator.clear()
        self.display.update_display("")

    def handle_equal(self) -> None:
        """Evaluate and display the result of the current equation."""
        result = self.calculator.solve()
        self.display.update_display(result)

    def handle_append(self, value: str) -> None:
        """Append a value to the calculator's entry."""
        self.calculator.append(value)
        self.display.update_display(self.calculator.entry_value)

    def handle_conversion(self, operation: str) -> None:
        """
        Execute a conversion operation using the appropriate strategy.

        Args:
            operation (str): The name of the conversion operation.
        """
        try:
            value = float(self.calculator.entry_value)
            strategy_map = {
                "Mi to Km": MilesToKmStrategy(),
                "Km to Mi": KmToMilesStrategy(),
                "C to F": CelsiusToFahrenheitStrategy(),
                "F to C": FahrenheitToCelsiusStrategy(),
                "In to Cm": InchesToCentimeters(),
                "Cm to In": CentimetersToInches(),
                "Min to Sec": MinutesToSecondsStrategy(),
                "Sec to Min": SecondsToMinutesStrategy()
            }
            self.conversion_context.set_strategy(strategy_map[operation])
            result = self.conversion_context.execute_conversion(value)
            self.display.update_display(result)
        except ValueError:
            self.display.update_display("Error")


# ------------------ UI Components ------------------

class Display:
    """Handles the display and menu."""

    def __init__(self, master: Tk, mediator: AppMediator) -> None:
        self.mediator = mediator
        self.equation = StringVar(value="")
        self.create_display(master)
        self.create_menu(master)
        self.configure_window(master)

    def configure_window(self, master: Tk) -> None:
        """Configure the main tkinter window."""
        master.title("Calculator")
        master.geometry('380x570+0+0')
        master.config(bg='#484F2B')
        master.resizable(False, False)

    def create_display(self, master: Tk) -> None:
        """Create the display entry widget."""
        self.entry = Entry(
            master, width=17, bg='#AEBD93', font=('Helvetica Bold', 28),
            relief='flat', textvariable=self.equation
        )
        self.entry.place(x=10, y=50, width=360, height=70)

    def create_menu(self, master: Tk) -> None:
        """Create the menu for switching modes."""
        menu = Frame(master, bg='#484F2B')
        menu.place(x=10, y=10, width=380, height=30)

        Button(
            menu, text="Standard", bg='#7A8450', fg='white',
            command=self.mediator.set_standard_mode, relief='flat'
        ).pack(side='left', padx=5)

        Button(
            menu, text="Convert", bg='#7A8450', fg='white',
            command=self.mediator.set_convert_mode, relief='flat'
        ).place(x=275)

    def update_display(self, value: Union[str, float]) -> None:
        """Update the display with a given value."""
        if isinstance(value, (float, int)):
            self.equation.set(f"{value:.3f}")
        else:
            self.equation.set(str(value))


class ButtonManager:
    """Handles button creation and management."""

    def __init__(self, master: Tk, mediator: AppMediator) -> None:
        self.mediator = mediator
        self.button_frame = Frame(master, bg='#484F2B')
        self.button_frame.place(x=10, y=125, width=360, height=440)
        self.update_buttons()

    def update_buttons(self) -> None:
        """Create buttons dynamically based on the current mode."""
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        buttons = self.mediator.mode.create_buttons()
        for text, row, col in buttons:
            if "to" in text:
                self.create_conversion_button(text, row, col)
            else:
                self.create_standard_button(text, row, col)

    def create_standard_button(self, text: str, row: int, col: int) -> None:
        """Create a standard calculator button."""
        def handle_command() -> None:
            if text == 'C':
                self.mediator.handle_clear()
            elif text == '=':
                self.mediator.handle_equal()
            else:
                self.mediator.handle_append(text)

        Button(
            self.button_frame, width=7, height=4, text=text, relief='flat',
            bg='#7A8450', activebackground='#AEBD93', fg='white',
            bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
            command=handle_command
        ).grid(column=col, row=row, padx=4, pady=4)

    def create_conversion_button(self, text: str, row: int, col: int) -> None:
        """Create a conversion calculator button."""
        def handle_conversion() -> None:
            self.mediator.handle_conversion(text)

        Button(
            self.button_frame, width=7, height=4, text=text, relief='flat',
            bg='white', activebackground='white', fg='black',
            bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
            command=handle_conversion
        ).grid(column=col, row=row, padx=4, pady=4)


# ------------------ Main Application ------------------

if __name__ == "__main__":
    root = Tk()
    mediator = AppMediator(root)
    root.mainloop()
