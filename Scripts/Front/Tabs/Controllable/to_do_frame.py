import customtkinter

from Scripts.Utils.events_handler import register_handler


class ToDoFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind('<Configure>', self.adjust_width)

        self.date_label = customtkinter.CTkLabel(master=self, text="Date")
        self.time_label = customtkinter.CTkLabel(master=self, text="Time")
        self.text_label = customtkinter.CTkLabel(master=self, text="Text")
        self.complete_label = customtkinter.CTkLabel(master=self, text="Is Complete")

        #self.date_label.grid(row=0, column=0)
        #self.time_label.grid(row=0, column=1)
        #self.text_label.grid(row=0, column=2)
        #self.complete_label.grid(row=0, column=3)

        self.text_list = []
        self.date_list = []
        self.time_list = []
        self.complete_list = []

        register_handler('to_do_list_added', self.add)
        register_handler('to_do_list_populated', self.fill)

    def fill(self, list):
        for item in list:
            self.add(item)

        print(self.winfo_height())
        print(self.master.master.winfo_height())

    def add(self, item):
        y = len(self.text_list)

        text = customtkinter.CTkLabel(master=self, text=item.text, wraplength=500, height=50)
        date = customtkinter.CTkLabel(master=self, text=item.date, bg_color='green', padx=5)
        time = customtkinter.CTkLabel(master=self, text=item.time, bg_color='yellow', padx=5)
        complete = customtkinter.CTkCheckBox(master=self, text='',
                                             variable=customtkinter.BooleanVar(value=item.completed),
                                             checkbox_width=15, checkbox_height=15, corner_radius=1,
                                             width=15, bg_color='red')

        #date.place(relwidth=0.2, y=y)
        #time.place(relwidth=0.2, y=y, relx=0.2)
        #text.place(relwidth=0.5, y=y, relx=0.4)
        #complete.place(relwidth=0.1, y=y, relx=0.9)

        text.pack()

        self.text_list.append(text)
        self.date_list.append(date)
        self.time_list.append(time)
        self.complete_list.append(complete)

        self.update()

    def items_count(self):
        return len(self.text_list)

    def adjust_width(self, event):
        pass
        # self.grid_rowconfigure(index=0)
        #
        # for i in range(len(self.text_list)):
        #     text = self.text_list[i]
        #     text.configure(wraplength=self.winfo_width())
