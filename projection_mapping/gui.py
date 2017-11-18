#!/usr/bin/env python3
import sys
from PIL import Image, ImageTk
if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    import tkinter as tk

class Fullscreen_Window:

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.attributes('-fullscreen', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        self.tk.configure(background='black')
        self.frame = tk.Frame(self.tk)
        self.frame.pack()
        self.state = True
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = Fullscreen_Window()


    img = ImageTk.PhotoImage(Image.open("test_image.jpg").resize((720,720), Image.ANTIALIAS))
    panel = tk.Label(w.tk, image=img)
    panel.pack()


    w.tk.mainloop()
