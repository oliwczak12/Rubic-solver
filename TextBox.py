from tkinter import Label

class TextBox(Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        