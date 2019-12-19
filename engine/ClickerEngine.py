import math

import pyautogui

class ClickerEngine:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def open_portal_precentage(self):
        pyautogui.click(self.x + math.floor(self.w*0.59),
                                            self.y + math.floor(self.h*0.90))

