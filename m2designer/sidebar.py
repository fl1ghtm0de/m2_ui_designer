import customtkinter as ctk
from Signal import Signal

class Sidebar(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widget_signal = Signal(dict)

        self.configure(width=200, corner_radius=0)

    def insert_entry_text(self, entry:ctk.CTkEntry, text):
        if not isinstance(text, str):
            text = str(text)

        entry.delete(0, ctk.END)
        entry.insert(0, text)

class SidebarLeft(Sidebar):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.logo_label = ctk.CTkLabel(self, text="m2 ui designer\nby flightm0de", font=("Helvetica", 16, "bold"))
        self.logo_label.pack(pady=20, padx=10)

        self.frame_btn = ctk.CTkButton(self, text="Board", command=lambda: self.create_widget_signal.emit({"_type": "board", "width" : 100, "height" : 100}))
        self.frame_btn.pack(pady=10, padx=10)

        self.thinboard_btn = ctk.CTkButton(self, text="Thinboard", command=lambda: self.create_widget_signal.emit({"_type": "thinboard", "width" : 100, "height" : 100}))
        self.thinboard_btn.pack(pady=10, padx=10)

        self.big_btn = ctk.CTkButton(self, text="Button Big", command=lambda: self.create_widget_signal.emit({"_type": "button", "button_type": "big"}))
        self.big_btn.pack(pady=10, padx=10)

        self.large_btn = ctk.CTkButton(self, text="Button Large", command=lambda: self.create_widget_signal.emit({"_type": "button", "button_type": "large"}))
        self.large_btn.pack(pady=10, padx=10)

        self.middle_btn = ctk.CTkButton(self, text="Button Middle", command=lambda: self.create_widget_signal.emit({"_type": "button", "button_type": "middle"}))
        self.middle_btn.pack(pady=10, padx=10)

        self.small_btn = ctk.CTkButton(self, text="Button Small", command=lambda: self.create_widget_signal.emit({"_type": "button", "button_type": "small"}))
        self.small_btn.pack(pady=10, padx=10)

        self.small_thin_btn = ctk.CTkButton(self, text="Button Small_Thin", command=lambda: self.create_widget_signal.emit({"_type": "button", "button_type": "small_thin"}))
        self.small_thin_btn.pack(pady=10, padx=10)

        self.xlarge_btn = ctk.CTkButton(self, text="Button XLarge", command=lambda: self.create_widget_signal.emit({"_type": "button", "button_type": "xlarge"}))
        self.xlarge_btn.pack(pady=10, padx=10)

        self.xlarge_thin_btn = ctk.CTkButton(self, text="Button XLarge_Thin", command=lambda: self.create_widget_signal.emit({"_type": "button", "button_type": "xlarge_thin"}))
        self.xlarge_thin_btn.pack(pady=10, padx=10)

        self.xsmall_btn = ctk.CTkButton(self, text="Button XSmall", command=lambda: self.create_widget_signal.emit({"_type": "button", "button_type": "xsmall"}))
        self.xsmall_btn.pack(pady=10, padx=10)

class SidebarBottom(Sidebar):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for entries
        self.entries_frame = ctk.CTkFrame(self)
        self.entries_frame.pack(pady=10, padx=10, fill="x")

        self.x_entry = ctk.CTkEntry(self.entries_frame, placeholder_text="X")
        self.x_entry.pack(side="left", padx=5, expand=True, fill="x")
        self.x_entry

        self.y_entry = ctk.CTkEntry(self.entries_frame, placeholder_text="Y")
        self.y_entry.pack(side="left", padx=5, expand=True, fill="x")

        self.width_entry = ctk.CTkEntry(self.entries_frame, placeholder_text="Width")
        self.width_entry.pack(side="left", padx=5, expand=True, fill="x")

        self.height_entry = ctk.CTkEntry(self.entries_frame, placeholder_text="Height")
        self.height_entry.pack(side="left", padx=5, expand=True, fill="x")

        self.type_entry = ctk.CTkEntry(self.entries_frame, placeholder_text="Type")
        self.type_entry.pack(side="left", padx=5, expand=True, fill="x")

        self.parent_entry = ctk.CTkEntry(self.entries_frame, placeholder_text="Parent")
        self.parent_entry.pack(side="left", padx=5, expand=True, fill="x")

    def set_entry_values(self, x, y, width, height, type, parent):
        self.insert_entry_text(self.x_entry, f"X: {x}")
        self.insert_entry_text(self.y_entry, f"Y: {y}")
        self.insert_entry_text(self.width_entry, f"Width: {width}")
        self.insert_entry_text(self.height_entry, f"Height: {height}")
        self.insert_entry_text(self.type_entry, f"Type: {type}")
        self.insert_entry_text(self.parent_entry, f"Parent: {parent}")