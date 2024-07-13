import customtkinter
from components.draggableLabel import DraggableLabel
from components.mainWindow import MainWindowLabel
from components.buttonLabel import Button
from WidgetRelationshipManager import WidgetRelationshipManager
from Signal import Signal

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class View:
    def __init__(self):
        self.wrm = WidgetRelationshipManager()
        self.__setup_ui()

    def __setup_ui(self):
        self.app = customtkinter.CTk()
        self.app.geometry("2000x500")
        self.mainLabel = MainWindowLabel(master=self.app, text="main1", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height, width=400, height=400)
        self.mainLabel.place(x=0, y=0)
        self.mainLabel.dragged_signal.connect(self.move_widget)
        self.wrm.add_widget(self.mainLabel)

        self.mainLabel2 = MainWindowLabel(master=self.app, text="main2", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height, width=400, height=400)
        self.mainLabel2.place(x=405, y=0)
        self.mainLabel2.dragged_signal.connect(self.move_widget)

        self.mainLabel3 = MainWindowLabel(master=self.app, text="main3", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height, width=400, height=400)
        self.mainLabel3.place(x=810, y=0)
        self.mainLabel3.dragged_signal.connect(self.move_widget)

        self.wrm.add_child_widget(self.mainLabel, widget=self.mainLabel2)
        self.wrm.add_child_widget(self.mainLabel, self.mainLabel2, widget=self.mainLabel3)

        # self.mainLabel2 = MainWindowLabel(master=self.mainLabel, text="main2", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height, width=300, height=300)
        # self.mainLabel2.place(x=10, y=10)
        # mainLabel2 = MainWindowLabel(master=mainLabel, text="main2", parent_width_callback=app.winfo_width, parent_height_callback=app.winfo_height, width=100, height=200)
        # mainLabel2.place(x=150, y=100, anchor=customtkinter.CENTER)

        # btnTest = Button(master=mainLabel2, text="btn1", button_type="large", parent_width_callback=app.winfo_width, parent_height_callback=app.winfo_height)
        # btnTest.place(x=30, y=100, anchor=customtkinter.CENTER)

        # self.btnX = Button(master=self.app, text="btnX", button_type="xsmall", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height)
        # self.btnX.place(x=810, y=0)

        # self.btnY = Button(master=self.app, text="btnY", button_type="xsmall", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height)
        # self.btnY.place(x=870, y=0)

        self.app.mainloop()

    def move_widget(self, widget, x, y):
        # FIX MOVING WIDGETS !!! ----------------------------------------------------------
        # ----------------------------------------------------------
        # ----------------------------------------------------------
        # ----------------------------------------------------------
        children = self.wrm.get_child_widgets(widget)
        for key, value in children.items():
            key.place(x=x, y=y)

    def create_mainwindow_label(self):
        pass
