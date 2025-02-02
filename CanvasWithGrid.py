from tkinter import Canvas, Button

from Grid import Grid

import globals


class CanvasWithGrid(Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid = Grid()
        self.color_swich = False
        self.colorSwich = Button(
            self,
            text="Color",
            command = self.swichColor,
            activebackground="blue",
            activeforeground="white",
            anchor="center",
            bd=3,
            bg="lightgray",
            cursor="hand2",
            disabledforeground="gray",
            fg="black",
            font=("Arial", 12),
            height=2,
            highlightbackground="black",
            highlightcolor="green",
            highlightthickness=2,
            justify="center",
            overrelief="raised",
            padx=10,
            pady=5,
            width=15,
            wraplength=100,
        )
        
        self.colorSwich.place(x=globals.window_width // 2-200, y=globals.window_height - 150)
        
        self.rec_list = []

    def swichColor(self):
        self.color_swich = not self.color_swich
        