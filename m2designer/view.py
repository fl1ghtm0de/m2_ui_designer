import customtkinter
from widget_relationship_manager import WidgetRelationshipManager
from tkinter import Canvas, messagebox
from sidebar import SidebarLeft, SidebarRight
from ctk_signal import Signal

from config_loader import Config

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class View:
    def __init__(self):
        self.wrm = WidgetRelationshipManager()
        self.set_bottom_sidebar_values_signal = Signal(int, int, int, int, int, int, str)

        self.__setup_ui()

    def __setup_ui(self):
        """This should be the last call of the constructor, as the mainloop will block all calls invoked afterwards
        """
        self.app = customtkinter.CTk()
        self.app.geometry("1600x900")
        self.app.iconbitmap("icon.ico")
        self.app.title("m2designer")

        self.app.bind("<Left>", lambda e: self.on_arrow_drag(dx=-2, dy=0))
        self.app.bind("<Right>", lambda e: self.on_arrow_drag(dx=2, dy=0))
        self.app.bind("<Up>", lambda e: self.on_arrow_drag(dx=-0, dy=-2))
        self.app.bind("<Down>", lambda e: self.on_arrow_drag(dx=0, dy=2))

        self.sidebar_left = SidebarLeft(self.app)
        self.sidebar_left.pack(side="left", fill="y")

        # self.sidebar_bottom = SidebarBottom(self.app)
        # self.sidebar_bottom.pack(side="bottom", fill="x")

        self.sidebar_right = SidebarRight(self.app)
        self.sidebar_right.pack(side="right", fill="y")
        self.sidebar_right.show_error_signal.connect(lambda title, msg: messagebox.showerror(title, msg))
        self.sidebar_right.entry_input_signal.connect(self.wrm.apply_entry_input)

        self.canvas = Canvas(self.app, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.focus_set()
        self.set_canvas_background()
        self.wrm.set_canvas(self.canvas)

        self.sidebar_left.create_widget_signal.connect(self.handle_sidebar_signal)
        self.sidebar_left.export_uiscript_signal.connect(self.wrm.parse_to_uiscript_format)
        # self.sidebar_bottom.entry_input_signal.connect(self.wrm.move_widget_absolute)
        # self.set_bottom_sidebar_values_signal.connect(self.sidebar_bottom.set_entry_values)
        self.wrm.clicked_signal.connect(self.sidebar_right.set_entry_values)
        self.wrm.error_message_signal.connect(lambda title, msg: messagebox.showerror(title, msg))
        # w = self.wrm.create_widget(_type="board", canvas=self.canvas, x=100, y=100, width=600, height=600)
        # b1 = self.wrm.create_widget(_type="button", button_type="large", canvas=self.canvas, x=10, y=10, parent=w)
        # a = self.wrm.create_widget(_type="board", canvas=self.canvas, x=10, y=200, width=30, height=30, parent=w)
        # b = self.wrm.create_widget(_type="board", canvas=self.canvas, x=45, y=200, width=30, height=30, parent=w)
        # w1_1 = self.wrm.create_widget(_type="board", canvas=self.canvas, x=10, y=10, width=180, height=40, parent=w1)
        # w1_2 = self.wrm.create_widget(_type="thinboard", canvas=self.canvas, x=75, y=55, width=130, height=40, parent=w1)

        self.app.mainloop()

    def set_canvas_background(self):
        """Set canvas background color based on the system appearance mode."""
        appearance_mode = customtkinter.get_appearance_mode()
        bg_color = "black" if appearance_mode == "Dark" else "white"
        self.canvas.config(bg=bg_color)

    def handle_sidebar_signal(self, _dict:dict):
        wdg = self.wrm.create_widget(**_dict, canvas=self.canvas, x=20, y=20)
        self.wrm.hide_handles(self.wrm.get_curr_widget())
        self.wrm.set_curr_widget(wdg)
        self.wrm.show_handles(wdg)

    def on_arrow_drag(self, dx, dy):
        wdg = self.wrm.get_curr_widget()
        if wdg is not None:
            wdg.arrow_drag_signal.emit(dx, dy)

