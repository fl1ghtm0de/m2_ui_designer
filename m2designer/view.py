import customtkinter
from components.draggableLabel import DraggableLabel
from components.mainWindow import MainWindowLabel
from components.buttonLabel import Button
from WidgetRelationshipManager import WidgetRelationshipManager
from Signal import Signal
from tools.utils import flattenDict
from tkinter import Canvas
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
        self.canvas = Canvas(self.app, width=800, height=600, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.mainLabel = MainWindowLabel(canvas=self.canvas, text="label 1", x=20, y=20, width=500, height=500)
        self.mainLabel.dragged_signal.connect(self.move_widget)

        self.mainLabel2 = MainWindowLabel(parent=self.mainLabel, canvas=self.canvas, text="label 2", x=20, y=20, width=400, height=400)
        self.mainLabel2.dragged_signal.connect(self.move_widget)

        self.mainLabel3 = MainWindowLabel(parent=self.mainLabel2, canvas=self.canvas, text="label 2", x=20, y=20, width=300, height=300)
        self.mainLabel3.dragged_signal.connect(self.move_widget)

        self.mainLabel4 = MainWindowLabel(parent=self.mainLabel3, canvas=self.canvas, text="label 2", x=20, y=20, width=200, height=200)
        self.mainLabel4.dragged_signal.connect(self.move_widget)

        self.mainLabel5 = MainWindowLabel(parent=self.mainLabel4, canvas=self.canvas, text="label 2", x=20, y=20, width=45, height=100)
        self.mainLabel5.dragged_signal.connect(self.move_widget)

        self.mainLabel6 = MainWindowLabel(parent=self.mainLabel4, canvas=self.canvas, text="label 2", x=55, y=20, width=45, height=100)
        self.mainLabel6.dragged_signal.connect(self.move_widget)

        self.btn = Button(parent=self.mainLabel3, canvas=self.canvas, button_type="large", text="button 1", x=125, y=20)
        self.btn.dragged_signal.connect(self.move_widget)

        # print(self.wrm.widgets)

        # self.mainLabel6 = MainWindowLabel(parent=self.mainLabel5, canvas=self.canvas, text="label 2", x=20, y=20, width=10, height=10)
        # self.mainLabel6.dragged_signal.connect(self.move_widget)

        self.app.mainloop()

    def move_widget(self, widget:DraggableLabel, x, y):
        # print(image_id, x, y)
        self.canvas.move(widget.image_id, x, y)
        # print(self.canvas.coords(widget.image_id))
        # Get the initial position of the parent widget
        # initial_place_info = widget.place_info()
        # initial_x = int(initial_place_info["x"])
        # initial_y = int(initial_place_info["y"])
        # width_widget = widget.winfo_width()
        # height_widget = widget.winfo_height()

        # # Calculate the offset due to the movement
        # offset_x = x - initial_x
        # offset_y = y - initial_y
        # # Move the parent widget to the new position
        # widget.place(x=x, y=y)

        # # Get the child widgets and move them accordingly
        children = flattenDict(self.wrm.get_child_widgets(widget))
        print(children)
        if children:
            for child in children:
                self.canvas.move(child.image_id, x, y)
        #         child_place_info = child.place_info()
        #         x_child = int(child_place_info["x"])
        #         y_child = int(child_place_info["y"])

        #         # Move the child widget by the same offset
        #         x_new_child = x_child + offset_x
        #         y_new_child = y_child + offset_y

        #         width_child = child.winfo_width()
        #         height_child = child.winfo_height()

        #         if (x_new_child + width_child < initial_x + width_widget) and (x_new_child > initial_x):
        #             child.place(x=x_child + offset_x, y=y_child + offset_y)


    def create_mainwindow_label(self):
        pass
