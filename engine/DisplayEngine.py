import cv2
import pywintypes
import win32api
import win32con
import tkinter as tk

from random import seed, choice
from string import ascii_letters

def display_sample_text(x = 0,y = 0):
    label = tk.Label(text='Text on the screen', font=('Times New Roman', '40'), fg='green', bg='white')
    label.master.overrideredirect(True)
    label.master.geometry("+{0}+{1}".format(x,y))
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()
    label.mainloop()

def display_text(display_text, x = 0,y = 0):
    label = tk.Label(text=display_text, font=('Times New Roman', '40'), fg='green', bg='white')
    label.master.overrideredirect(True)
    label.master.geometry("+{0}+{1}".format(x,y))
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()
    label.mainloop()


def display_dots_on_img(img,cords,colour):
    temp = img.copy()
    for c in cords:
        cv2.circle(temp, (c[0], c[1]), 5, colour, 3)
    return temp

def display_msg(img,cords,msg,colour=(0,0,255)):
    temp = img.copy()
    for c in cords:
        cv2.putText(temp,msg, (c[0],c[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, colour,3,cv2.LINE_AA)
    return temp


class DisplayEngine:

    def __init__(self):
        self.k = 1

