from PIL import ImageGrab
from numpy import uint8
from numpy.ma import array


def get_screen_img(x1,y1,x2,y2):
    box = (x1, y1, x2, y2)
    screen = ImageGrab.grab(box)
    img = array(screen.getdata(), dtype=uint8).reshape((screen.size[1], screen.size[0], 3))
    return img