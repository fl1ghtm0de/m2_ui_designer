import customtkinter
from components.draggableLabel import DraggableLabel
from components.mainWindow import MainWindowLabel
from components.buttonLabel import Button
from WidgetRelationshipManager import WidgetRelationshipManager
from Signal import Signal
from tools.utils import flattenDict
import threading

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

        self.mainLabel2 = MainWindowLabel(master=self.app, text="main2", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height, width=200, height=100)
        self.mainLabel2.place(x=405, y=0)
        self.mainLabel2.dragged_signal.connect(self.move_widget)

        self.mainLabel3 = MainWindowLabel(master=self.app, text="main3", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height, width=80, height=80)
        self.mainLabel3.place(x=810, y=0)
        self.mainLabel3.dragged_signal.connect(self.move_widget)

        self.mainLabel4 = MainWindowLabel(master=self.app, text="main4", parent_width_callback=self.app.winfo_width, parent_height_callback=self.app.winfo_height, width=40, height=40)
        self.mainLabel4.place(x=810, y=0)
        self.mainLabel4.dragged_signal.connect(self.move_widget)

        self.wrm.add_child_widget(self.mainLabel, self.mainLabel3, self.mainLabel2)
        self.wrm.add_child_widget(self.mainLabel3, self.mainLabel4)
        # self.wrm.add_child_widget(self.mainLabel3, self.mainLabel4)
        # self.wrm.add_child_widget(self.mainLabel2, self.mainLabel)
        # self.wrm.add_child_widget(self.mainLabel2, self.mainLabel4)
        # self.wrm.add_child_widget(self.mainLabel3, self.mainLabel, self.mainLabel2)

        # print(self.wrm.widgets[self.mainLabel][self.mainLabel2])

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
        # Get the initial position of the parent widget
        initial_place_info = widget.place_info()
        initial_x = int(initial_place_info["x"])
        initial_y = int(initial_place_info["y"])
        width_widget = widget.winfo_width()
        height_widget = widget.winfo_height()

        # Calculate the offset due to the movement
        offset_x = x - initial_x
        offset_y = y - initial_y
        # Move the parent widget to the new position
        widget.place(x=x, y=y)

        # Get the child widgets and move them accordingly
        children = flattenDict(self.wrm.get_child_widgets(widget))
        if children:
            for child in children:
                child_place_info = child.place_info()
                x_child = int(child_place_info["x"])
                y_child = int(child_place_info["y"])

                # Move the child widget by the same offset
                x_new_child = x_child + offset_x
                y_new_child = y_child + offset_y

                width_child = child.winfo_width()
                height_child = child.winfo_height()

                if (x_new_child + width_child < initial_x + width_widget) and (x_new_child > initial_x):
                    child.place(x=x_child + offset_x, y=y_child + offset_y)


    def create_mainwindow_label(self):
        pass
