from tkinter import Tk, Entry, Button, StringVar, Frame


# ------------------ Base Logic ------------------

class CalculatorBase:
    """Handles the core mathematical operations of the calculator."""
    def __init__(self):
        self.entry_value = ''

    def append(self, value):
        self.entry_value += str(value)

    def clear(self):
        self.entry_value = ''

    def solve(self):
        try:
            return eval(self.entry_value)
        except Exception:
            return "Error"


# ------------------ Conversion Logic ------------------

class ConversionContext:
    """Manages the selection and execution of a conversion strategy."""
    def __init__(self):
        self.strategy_map = {
            "Mi to Km": self.miles_to_km,
            "Km to Mi": self.km_to_miles,
            "C to F": self.celsius_to_fahrenheit,
            "F to C": self.fahrenheit_to_celsius,
        }

    @staticmethod
    def miles_to_km(val):
        return val * 1.60934

    @staticmethod
    def km_to_miles(val):
        return val / 1.60934

    @staticmethod
    def celsius_to_fahrenheit(val):
        return (val * 9 / 5) + 32

    @staticmethod
    def fahrenheit_to_celsius(val):
        return (val - 32) * 5 / 9

    def execute_conversion(self, operation, val):
        strategy = self.strategy_map.get(operation)
        if not strategy:
            raise ValueError(f"Invalid operation: {operation}")
        return strategy(val)


# ------------------ Modes for Buttons ------------------

class CalculatorMode:
    """Defines a common interface for calculator modes."""
    def create_buttons(self):
        raise NotImplementedError("Subclasses must implement this method.")


class StandardMode(CalculatorMode):
    """Defines buttons for the standard calculator mode."""
    def create_buttons(self):
        return [
            ('(', 0, 0), (')', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('.', 4, 2), ('=', 4, 3),
        ]


class ConvertMode(CalculatorMode):
    """Defines buttons for the conversion calculator mode."""
    def create_buttons(self):
        return [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('C', 4, 0), ('0', 4, 1), ('.', 4, 2),
            ('Mi to Km', 0, 0), ('Km to Mi', 0, 1),
            ('C to F', 0, 2), ('F to C', 0, 3),
        ]


# ------------------ Mediator ------------------

class AppMediator:
    """Central mediator for managing the application state and communication."""
    def __init__(self, master):
        self.calculator = CalculatorBase()
        self.conversion_context = ConversionContext()
        self.mode = StandardMode()  # Default mode
        self.display = Display(master, self)
        self.button_manager = ButtonManager(master, self)

    # Mode management
    def set_standard_mode(self):
        self.mode = StandardMode()
        self.button_manager.update_buttons()

    def set_convert_mode(self):
        self.mode = ConvertMode()
        self.button_manager.update_buttons()

    # Calculator operations
    def handle_clear(self):
        self.calculator.clear()
        self.display.update_display("")

    def handle_equal(self):
        result = self.calculator.solve()
        self.display.update_display(result)

    def handle_append(self, value):
        self.calculator.append(value)
        self.display.update_display(self.calculator.entry_value)

    def handle_conversion(self, operation):
        try:
            value = float(self.calculator.entry_value)
            result = self.conversion_context.execute_conversion(operation, value)
            self.display.update_display(f"{result:.2f}")
        except ValueError:
            self.display.update_display("Error")


# ------------------ UI Components ------------------

class Display:
    """Handles the display and menu."""
    def __init__(self, master, mediator):
        self.mediator = mediator
        self.equation = StringVar()
        self.create_display(master)
        self.create_menu(master)
        self.configure_window(master)

    def configure_window(self, master):
        master.title("Calculator")
        master.geometry('380x570+0+0')
        master.config(bg='#484F2B')
        master.resizable(False, False)

    def create_display(self, master):
        self.entry = Entry(
            master, width=17, bg='#AEBD93', font=('Helvetica Bold', 28),
            relief='flat', textvariable=self.equation
        )
        self.entry.place(x=10, y=50, width=360, height=70)

    def create_menu(self, master):
        menu = Frame(master, bg='#484F2B')
        menu.place(x=10, y=10, width=380, height=30)

        Button(
            menu, text="Standard", bg='#7A8450', fg='white',
            command=self.mediator.set_standard_mode, relief='flat'
        ).pack(side='left', padx=5)

        Button(
            menu, text="Convert", bg='#7A8450', fg='white',
            command=self.mediator.set_convert_mode, relief='flat'
        ).pack(side='left', padx=5)

    def update_display(self, value):
        self.equation.set(value)


class ButtonManager:
    """Handles button creation and management."""
    def __init__(self, master, mediator):
        self.mediator = mediator
        self.button_frame = Frame(master, bg='#484F2B')
        self.button_frame.place(x=10, y=125, width=360, height=440)
        self.update_buttons()

    def update_buttons(self):
        """Create buttons dynamically based on the current mode."""
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        buttons = self.mediator.mode.create_buttons()
        for text, row, col in buttons:
            if "to" in text:
                self.create_conversion_button(text, row, col)
            else:
                self.create_standard_button(text, row, col)

    def create_standard_button(self, text, row, col):
        """Create a standard calculator button."""
        if text == 'C':
            command = self.mediator.handle_clear
        elif text == '=':
            command = self.mediator.handle_equal
        else:
            command = lambda: self.mediator.handle_append(text)

        Button(
            self.button_frame, width=7, height=4, text=text, relief='flat',
            bg='#7A8450', activebackground='#AEBD93', fg='white',
            bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
            command=command
        ).grid(column=col, row=row, padx=4, pady=4)

    def create_conversion_button(self, text, row, col):
        """Create a conversion calculator button."""
        command = lambda: self.mediator.handle_conversion(text)
        Button(
            self.button_frame, width=7, height=4, text=text, relief='flat',
            bg='white', activebackground='white', fg='black',
            bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
            command=command
        ).grid(column=col, row=row, padx=4, pady=4)


# ------------------ Main Application ------------------

if __name__ == "__main__":
    root = Tk()
    mediator = AppMediator(root)
    root.mainloop()