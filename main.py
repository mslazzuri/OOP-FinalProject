from calculator import AppMediator
from tkinter import Tk

# ------------------ Main Application ------------------

if __name__ == "__main__":
    root = Tk()
    mediator = AppMediator(root)
    root.mainloop()