import customtkinter
from WidgetRelationshipManager import WidgetRelationshipManager
from tkinter import Canvas
from tools.utils import flattenDict
from sidebar import SidebarLeft, SidebarBottom
from Signal import Signal

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class View:
    def __init__(self):
        self.wrm = WidgetRelationshipManager()
        self.set_bottom_sidebar_values_signal = Signal(int, int, int, int, str)
        self.type_widget_map = {
            "frame" : self.wrm.create_window,
            "button" : self.wrm.create_button,
            "textfield" : None
        }

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

        w = self.wrm.create_window(100, 100, 600, 600, text="w")
        w1 = self.wrm.create_window(10, 10, 200, 140, parent=w, text="w1")
        b1 = self.wrm.create_button(10, 10, parent=w, text="b1")
        a = self.wrm.create_window(10, 200, 30, 30, parent=w, text="a")
        b = self.wrm.create_window(45, 200, 30, 30, parent=w, text="b")
        w1_1 = self.wrm.create_window(10, 10, 180, 40, parent=w1, text="w1_1")
        w1_2 = self.wrm.create_window(75, 55, 130, 40, parent=w1, text="w1_2")

        print(self.wrm.widgets)

        self.app.mainloop()

    def handle_sidebar_signal(self, _type):
        _func = self.type_widget_map.get(_type, None)
        if _func is not None:
            _func()

    def on_arrow_drag(self, dx, dy):
        wdg = self.wrm.get_curr_widget()
        if wdg is not None:
            wdg.arrow_drag_signal.emit(dx, dy)

