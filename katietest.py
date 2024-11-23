from tkinter import Tk, Entry, Button, StringVar, Frame

class CalculatorBase:
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


class ConversionMethods:
    @staticmethod
    def miles_to_km(val):
        return val * 1.60934

    @staticmethod
    def km_to_miles(val):
        return val / 1.60934

    @staticmethod
    def cel_to_fahr(val):
        return (val * 9/5) + 32

    @staticmethod
    def fahr_to_cel(val):
        return (val - 32) * 5/9


class Display:
    def __init__(self, master):
        self.master = master
        self.equation = StringVar()
        self.mode = "Standard"
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
            command=lambda: self.set_mode("Standard"), relief='flat'
        ).pack(side='left', padx=5)

        Button(
            menu, text="Convert", bg='#7A8450', fg='white',
            command=lambda: self.set_mode("Conversion"), relief='flat'
        ).place(x=275)

    def set_mode(self, mode):
        self.mode = mode
        ButtonManager(self.master, CalculatorBase(), self)

    def update_display(self, value):
        self.equation.set(value)


class ButtonManager:
    def __init__(self, master, calculator, display):
        self.master = master
        self.calculator = calculator
        self.display = display
        self.create_buttons()

    def create_buttons(self):
        button_frame = Frame(self.master, bg='#484F2B')
        button_frame.place(x=10, y=125, width=360, height=440)
        convert_buttons = []

        if self.display.mode == "Standard":
            buttons = [
                ('(', 0, 0), (')', 0, 1), ('%', 0, 2), ('/', 0, 3),
                ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
                ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
                ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
                ('0', 4, 0), ('C', 4, 1), ('.', 4, 2), ('=', 4, 3),
            ]
        else:
            buttons = [
                ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
                ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
                ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
                ('C', 4, 0), ('0', 4, 1), ('.', 4, 2)
            ]

            convert_buttons = [
                ('Mi to Km', 0, 0),
                ('Km to Mi', 0, 1),
                ('C to F', 0, 2),
                ('F to C', 0, 3),
            ]

        for widget in button_frame.winfo_children():
            widget.destroy()

        for text, row, col in buttons:
            self.create_button(button_frame, text, row, col)

        for text, row, col in convert_buttons:
            self.create_convert_button(button_frame, text, row, col)

    def create_button(self, button_frame, text, row, col):
        if text == 'C':
            command = self.clear
        elif text == '=':
            command = self.solve
        else:
            command = lambda t=text: self.append_value(t)

        Button(
            button_frame, width=7, height=4, text=text, relief='flat',
            bg='#7A8450', activebackground='#AEBD93', fg='white',
            bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
            command=command
        ).grid(column=col, row=row, padx=4, pady=4)

    def create_convert_button(self, button_frame, text, row, col):
        if text in ['Mi to Km', 'Km to Mi',
                    'C to F', 'F to C']:
            command = lambda t=text: self.convert(t)
        Button(
            button_frame, width=7, height=4, text=text, relief='flat',
            bg='white', activebackground='white', fg='black',
            bd=0, highlightbackground='#484F2B', highlightcolor='#7A8450',
            command=command
        ).grid(column=col, row=row, padx=4, pady=4)

    def append_value(self, value):
        self.calculator.append(value)
        self.display.update_display(self.calculator.entry_value)

    def clear(self):
        self.calculator.clear()
        self.display.update_display("")

    def solve(self):
        result = self.calculator.solve()
        self.display.update_display(result)

    def convert(self, operation):
        try:
            value = float(self.calculator.entry_value)
            if operation == "Mi to Km":
                result = ConversionMethods.miles_to_km(value)
            elif operation == "Km to Mi":
                result = ConversionMethods.km_to_miles(value)
            elif operation == "C to F":
                result = ConversionMethods.cel_to_fahr(value)
            elif operation == "F to C":
                result = ConversionMethods.fahr_to_cel(value)
            else:
                result = "Error"
            self.display.update_display(f"{result:.2f}")
        except ValueError:
            self.display.update_display("Error")


if __name__ == "__main__":
    root = Tk()
    calculator = CalculatorBase()
    display = Display(root)
    buttons = ButtonManager(root, calculator, display)
    root.mainloop()
