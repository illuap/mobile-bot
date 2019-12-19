import win32gui

from pynput.keyboard import Key, Listener

from grabber.ApplicationImageGrabber import ApplicationImageGrabber

AppImgGrabber = ApplicationImageGrabber("Nox")
win_info = AppImgGrabber.window_info

f = open("..\scripts\demofile1.txt", "x")


def get_mouse_pos():
    flags, hcursor, (x, y) = win32gui.GetCursorInfo()
    return (x,y)

def get_relative_pos():
    (x,y) = get_mouse_pos()
    return ( (x - win_info['x'])/win_info['width'],
             (y - win_info['y'])/win_info['height'])


def on_press(key):
    print('----------')
    if key == Key.space:
        print('({0},{1})'.format(get_relative_pos()[0], get_relative_pos()[1]))
        f.write('{0},{1} '.format(get_relative_pos()[0], get_relative_pos()[1]))

def on_release(key):
    if key == Key.space:
        print('({0},{1})'.format(get_relative_pos()[0], get_relative_pos()[1]))
        f.write('{0},{1} '.format(get_relative_pos()[0], get_relative_pos()[1]))
    if key == Key.esc:
        print('= Exiting =')
        f.close()
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()