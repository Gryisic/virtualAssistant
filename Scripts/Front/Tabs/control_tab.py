import customtkinter
import threading

from CTkListbox import CTkListbox
from tkinter import constants

from customtkinter import CTkSwitch

from Scripts.Utils.events_handler import register_handler


class ControlTab(customtkinter.CTkTabview):
    recognizer = None

    def __init__(self, **kwargs):
        super().__init__(master=kwargs['root'], height=150, command=lambda: self.tab_changed())
        self.pack(fill='x', side='bottom')
        self.add('General')
        self.add('Logs')

        self.recognizer = kwargs['recognizer']
        self.listbox = CTkListbox(master=self.tab('Logs'))
        self.listbox.pack(fill='x')

        switch = CTkSwitch(master=self.tab('General'), text='Enable recognition', onvalue='On', offvalue="Off",
                           command=lambda: self.toggle_recognition(switch))
        switch.place(relx=0.5, rely=0.5, anchor='center')

        register_handler('logs_updated', self.fill_logs)
        register_handler('stop_recognition', lambda: switch.toggle())

    def tab_changed(self):
        active_tab = self.get()

    def toggle_recognition(self, switch):
        if switch.get() == 'On':
            thread = threading.Thread(target=self.recognizer.start_listening, daemon=True)
            thread.start()
        else:
            self.recognizer.stop_listening()

    def fill_logs(self, logs):
        self.listbox.delete(0, constants.END)
        for i in range(len(logs) - 1, -1, -1):
            log = logs[i]
            self.listbox.insert(constants.END, log)

