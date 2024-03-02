from PIL import ImageGrab, Image
import win32gui


toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)


def grab_screen():
    opera = [(hwnd, title) for hwnd, title in winlist if 'opera' in title.lower()]
    # just grab the hwnd for first window matching opera
    opera = opera[0]
    hwnd = opera[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    #img.save('screenshot.png')
    return img