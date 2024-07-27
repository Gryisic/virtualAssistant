import win32gui
import win32con


def get_hwnd(window_title: str, foreground: bool):
    top_list = []
    win_list = []

    def enum_callback(hwnd, results):
        win_list.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_callback, top_list)

    if foreground:
        hwnd = win32gui.GetForegroundWindow()
    else:
        hwnd = [(hwnd, title) for hwnd, title in win_list if window_title in title.lower()][0][0]

    return hwnd


def min_max(minimize: bool, window_title: str = None, foreground: bool = False):
    hwnd = get_hwnd(window_title, foreground)
    index = win32con.SW_MINIMIZE if minimize else win32con.SW_MAXIMIZE
    win32gui.ShowWindow(hwnd, index)


def close_by_name(window_title: str):
    hwnd = get_hwnd(window_title, False)
    close(hwnd)


def close_active():
    hwnd = get_hwnd('', True)
    close(hwnd)


def close(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
