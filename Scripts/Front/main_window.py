import ctypes
import os
import pathlib
import tempfile
import pystray

from Scripts.Front.Tabs import control_tab
from customtkinter import CTk, CTkTabview, CTkSwitch
from pystray import MenuItem as MenuItem
from PIL import Image

icon = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00' * 1282 + b'\xff' * 64

_, icon_path = tempfile.mkstemp()


class MainWindow:
    root = None
    listbox = None
    recognizer = None

    def __init__(self, recognizer):
        self.recognizer = recognizer

    def quit_window(self, local_icon, item):
        local_icon.stop()
        self.root.quit()
        self.root.destroy()

    def show_window(self, local_icon, item):
        local_icon.stop()
        self.root.after(0, self.root.deiconify)

    def validate_path(self, path_to_validate, file_path=None):
        path = pathlib.Path().cwd()
        final_file_path = None

        while (not (path / path_to_validate).exists()) or (not (path / 'Scripts').exists()):
            path = path.parent

        if (path / path_to_validate).exists():
            final_file_path = path.joinpath(path_to_validate).joinpath(file_path)
        else:
            path = path.joinpath(path_to_validate)
            os.mkdir(path)
            final_file_path = path.joinpath(file_path)

        return final_file_path

    def on_closing(self):
        #self.root.quit()
        #self.root.destroy()
        self.root.withdraw()
        ctypes.windll['uxtheme.dll'][135](1)
        path = self.validate_path('LocalData\\images', 'va_icon.png')
        image = Image.open(path)
        menu = (MenuItem('Show', self.show_window, default=True), MenuItem('Quit', self.quit_window))
        local_icon = pystray.Icon('Icon', image, 'Assistant', menu)
        local_icon.run()

    def create(self):
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(icon)

        self.root = CTk()
        self.root.title('')
        self.root.iconbitmap(default=icon_path)
        #self.root.overrideredirect(True)

        kwargs = {
            'root': self.root,
            'recognizer': self.recognizer
        }
        control_tab.ControlTab(**kwargs)

        self.root.geometry('350x250')
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
        self.root.mainloop()
