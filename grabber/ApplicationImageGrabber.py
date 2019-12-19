from grabber import ImageGrabber
from grabber.ImageGrabber import get_screen_img
from grabber.WindowGrabber import WindowGrabber


class ApplicationImageGrabber:
    def __init__(self, window_substring):
        self.window_grabber = WindowGrabber(window_substring)
        self.window_info = self.window_grabber.get_window_info()

    def get_image(self):
        return ImageGrabber.get_screen_img(self.window_info['x'],
                                            self.window_info['y'],
                                            self.window_info['x'] + self.window_info['width'],
                                            self.window_info['y'] + self.window_info['height'])
