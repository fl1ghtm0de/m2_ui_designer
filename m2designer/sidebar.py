import customtkinter as ctk
from Signal import Signal

class Sidebar(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widget_signal = Signal(str)

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

        self.frame_btn = ctk.CTkButton(self, text="Frame", command=lambda: self.create_widget_signal.emit("frame"))
        self.frame_btn.pack(pady=10, padx=10)

        self.button_btn = ctk.CTkButton(self, text="Button", command=lambda: self.create_widget_signal.emit("button"))
        self.button_btn.pack(pady=10, padx=10)

        self.textfield_btn = ctk.CTkButton(self, text="Textfield", command=lambda: self.create_widget_signal.emit("textfield"))
        self.textfield_btn.pack(pady=10, padx=10)

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