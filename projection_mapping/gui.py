#!/usr/bin/env python3
import sys
import time
import numpy as np

from PIL import Image, ImageTk
if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    import tkinter as tk

class ImageApp(object):

    def __init__(self, root, img_path):
        self.tk = root
        self.tk.attributes('-fullscreen', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        self.tk.configure(background='black')
        self.state = True
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        self.l = tk.Label(root,width=1280,height=720)
        self.l.config(borderwidth=0)
        self.l.config(background='black')
        self.l.pack()
        self.path = img_path

        self.process_next_frame = self.draw().__next__
        root.after(1,self.process_next_frame)


    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def draw(self):
        img = Image.open(self.path)
        w, h = img.size

        if w > h: img = img.resize((720, int(round(720/w*h))),Image.ANTIALIAS)
        elif h > w: img =img.resize((int(round(720/h*w)),720),Image.ANTIALIAS)
        angle = 0 
        print(self.process_next_frame)

        while True:
            tkimg = ImageTk.PhotoImage(img.rotate(angle))
            self.l.configure(image=tkimg)
            self.l.pack()
            self.tk.after_idle(self.process_next_frame)
            yield
            #self.l.delete(canvas_obj)
            angle = (angle+5)%360


def find_coeffs(pa,pb):
    matrix = []
    for p1,p2 in zip(pa,pb):
        matrix.append([p1[0],p1[1],1,0,0,0,-p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0,0,0,p1[0],p1[1],1,-p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A)*A.T, B)
    return np.array(res).reshape(8)


if __name__ == '__main__':
    root=tk.Tk()
    root.attributes('-fullscreen',True)
    root.configure(background='black')
    # w = ImageApp(root,"test_image.jpg") #ImageApp(root,"dog_bg_black.jpg")

    img = Image.open("grid.jpg").resize((720,720),Image.ANTIALIAS)

    coeffs = find_coeffs(
#        [(100,0),(200,0),(200,200),(0,100)],
        [(50,0),(550,0),(600,600),(0,600)],
        [(0,0),(720,0),(720,720),(0,720)]
        )
 
    img = img.transform(img.size, Image.PERSPECTIVE,coeffs,Image.BICUBIC)

    tkimg = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=tkimg,width=1280,height=720)
    panel.config(borderwidth=0)
    panel.config(background='black')
    panel.pack()


    root.mainloop()
