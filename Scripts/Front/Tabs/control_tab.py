import customtkinter
import threading

from customtkinter import CTkSwitch
from Scripts.Front.Tabs.Controllable.logs_frame import LogsFrame
from Scripts.Front.Tabs.Controllable.to_do_frame import ToDoFrame
from Scripts.Utils.events_handler import register_handler, dispatch_event


class ControlTab(customtkinter.CTkTabview):
    recognizer = None

    def __init__(self, **kwargs):
        super().__init__(master=kwargs['root'], height=150, command=lambda: self.tab_changed())
        self.pack(fill='x', side='bottom')
        self.add('General')
        self.add('Logs')
        self.add('To-Do')

        self.recognizer = kwargs['recognizer']
        self.logs_frame = LogsFrame(master=self.tab('Logs'))
        self.logs_frame.pack(fill='x')

        self.to_do_frame = ToDoFrame(master=self.tab('To-Do'))
        self.to_do_frame.pack(fill='x')

        switch = CTkSwitch(master=self.tab('General'), text='Enable recognition', onvalue='On', offvalue="Off",
                           command=lambda: self.toggle_recognition(switch))
        switch.place(relx=0.5, rely=0.5, anchor='center')

        register_handler('logs_updated', self.logs_frame.add)
        register_handler('stop_recognition', lambda: switch.toggle())

    def tab_changed(self):
        active_tab = self.get()

        if active_tab == 'To-Do' and self.to_do_frame.items_count() <= 0:
            dispatch_event('to_do_list_requested')

    def toggle_recognition(self, switch):
        if switch.get() == 'On':
            thread = threading.Thread(target=self.recognizer.start_listening, daemon=True)
            thread.start()
        else:
            self.recognizer.stop_listening()
