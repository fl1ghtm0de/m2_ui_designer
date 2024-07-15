import customtkinter
from WidgetRelationshipManager import WidgetRelationshipManager
from tkinter import Canvas
from tools.utils import flattenDict
from sidebar import SidebarLeft, SidebarBottom
from Signal import Signal

from ConfigLoader import Config

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class View:
    def __init__(self):
        self.wrm = WidgetRelationshipManager()
        self.set_bottom_sidebar_values_signal = Signal(int, int, int, int, str)

        self.__setup_ui()

    def __setup_ui(self):
        """This should be the last call of the constructor, as the mainloop will block all calls invoked afterwards
        """
        self.app = customtkinter.CTk()
        self.app.geometry("1600x900")

        self.app.bind("<Left>", lambda e: self.on_arrow_drag(dx=-2, dy=0))
        self.app.bind("<Right>", lambda e: self.on_arrow_drag(dx=2, dy=0))
        self.app.bind("<Up>", lambda e: self.on_arrow_drag(dx=-0, dy=-2))
        self.app.bind("<Down>", lambda e: self.on_arrow_drag(dx=0, dy=2))

        self.sidebar_left = SidebarLeft(self.app)
        self.sidebar_left.pack(side="left", fill="y")

        self.sidebar_bottom = SidebarBottom(self.app)
        self.sidebar_bottom.pack(side="bottom", fill="x")

        self.canvas = Canvas(self.app, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.focus_set()
        self.wrm.set_canvas(self.canvas)

        self.sidebar_left.create_widget_signal.connect(self.handle_sidebar_signal)
        self.set_bottom_sidebar_values_signal.connect(self.sidebar_bottom.set_entry_values)
        self.wrm.clicked_signal.connect(self.sidebar_bottom.set_entry_values)

        # w = self.wrm.create_widget(_type="board", canvas=self.canvas, x=100, y=100, width=600, height=600)
        # w1 = self.wrm.create_widget(_type="board", canvas=self.canvas, x=10, y=10, width=200, height=140, parent=w, text="w1")
        # b1 = self.wrm.create_widget(_type="button", button_type="large", canvas=self.canvas, x=10, y=10, parent=w)
        # a = self.wrm.create_widget(_type="board", canvas=self.canvas, x=10, y=200, width=30, height=30, parent=w)
        # b = self.wrm.create_widget(_type="board", canvas=self.canvas, x=45, y=200, width=30, height=30, parent=w)
        # w1_1 = self.wrm.create_widget(_type="board", canvas=self.canvas, x=10, y=10, width=180, height=40, parent=w1)
        # w1_2 = self.wrm.create_widget(_type="thinboard", canvas=self.canvas, x=75, y=55, width=130, height=40, parent=w1)

        self.app.mainloop()

    def handle_sidebar_signal(self, _dict:dict):
        wdg = self.wrm.create_widget(**_dict, canvas=self.canvas, x=20, y=20)
        self.wrm.hide_handles(self.wrm.get_curr_widget())
        self.wrm.set_curr_widget(wdg)
        self.wrm.show_handles(wdg)

    def on_arrow_drag(self, dx, dy):
        wdg = self.wrm.get_curr_widget()
        if wdg is not None:
            wdg.arrow_drag_signal.emit(dx, dy)

