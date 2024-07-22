import customtkinter


class LogsFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind('<Configure>', self.adjust_width)
        self.label_list = []

    def add(self, logs):
        text = logs[-1]
        label = customtkinter.CTkLabel(master=self, text=text, wraplength=self.winfo_width())
        label.pack(fill='x')
        self.label_list.append(label)

    def adjust_width(self, event):
        for label in self.label_list:
            label.configure(wraplength=self.winfo_width())
