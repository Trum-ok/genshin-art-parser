import win32gui
import win32process
from pywinauto import Application


def get_window_pid(title):
    hwnd = win32gui.FindWindow(None, title)
    threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def activate_window():
    app = Application().connect(process=get_window_pid("Genshin Impact"))
    app.top_window().set_focus()


if __name__ == "__main__":
    activate_window()
