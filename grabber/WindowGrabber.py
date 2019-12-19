import win32gui


class WindowGrabber:
    def __init__(self, window_substring):
        self._windowSubStr = window_substring

    def get_window_info(self):
        window_info = {}
        win32gui.EnumWindows(self.set_window_coordinates, window_info)
        return window_info

    def set_window_coordinates(self,hwnd, window_info):
        if win32gui.IsWindowVisible(hwnd):
            if self._windowSubStr in win32gui.GetWindowText(hwnd):
                rect = win32gui.GetWindowRect(hwnd)
                x = rect[0]
                y = rect[1]
                w = rect[2] - x
                h = rect[3] - y
                window_info['x'] = x
                window_info['y'] = y
                window_info['width'] = w
                window_info['height'] = h
                window_info['name'] = win32gui.GetWindowText(hwnd)
                ##win32gui.SetForegroundWindow(hwnd)