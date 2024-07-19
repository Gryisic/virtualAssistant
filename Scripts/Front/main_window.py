import tempfile
import threading
from Scripts.Front.Tabs import control_tab

from customtkinter import CTk, CTkTabview, CTkSwitch

icon = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00' * 1282 + b'\xff' * 64

_, icon_path = tempfile.mkstemp()


class MainWindow:
    root = None
    listbox = None
    recognizer = None
    showing = False

    def __init__(self, recognizer):
        self.recognizer = recognizer

    def on_closing(self):
        self.showing = False
        self.root.quit()
        self.root.destroy()

    def create(self):
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(icon)

        self.root = CTk()
        self.root.title('')
        self.root.iconbitmap(default=icon_path)

        kwargs = {
            'root': self.root,
            'recognizer': self.recognizer
        }
        tab_view = control_tab.ControlTab(**kwargs)

        self.root.geometry('300x250')
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
        self.root.mainloop()
