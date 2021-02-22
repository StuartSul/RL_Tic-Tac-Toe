from tkinter import Label

class BoardSlot(Label):
    """Tkinter Label with location (i, j) info"""
    def __init__(self, master, i, j, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        self.i = i
        self.j = j