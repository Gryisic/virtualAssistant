from customtkinter import CTk, CTkTabview, CTkSwitch
import tempfile

icon = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, icon_path = tempfile.mkstemp()

class MainWindow:
    recognizer = None

    def set_recognizer(self, recognizer):
        self.recognizer = recognizer

    def create(self):
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(icon)

        root = CTk()
        root.title('')
        root.iconbitmap(default=icon_path)

        tab_view = CTkTabview(master=root, height=150)
        tab_view.pack(fill='x', side='bottom')
        tab_view.add('General')
        tab_view.add('Logs')

        def switch_event():
            self.recognizer.listen()

        switch = CTkSwitch(master=tab_view.tab('General'), text='Enable recognition', onvalue='On', offvalue="Off", command=switch_event)
        switch.place(relx=0.5, rely=0.5, anchor='center')

        root.geometry('300x250')
        root.mainloop()