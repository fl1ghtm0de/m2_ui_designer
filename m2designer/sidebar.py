import customtkinter as ctk
import tkinter as tk
from ctk_signal import Signal

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
        self.export_uiscript_signal = Signal()
        self.create_widgets()

    def create_widgets(self):
        self.logo_label = ctk.CTkLabel(self, text="m2 ui designer\nby flightm0de", font=("Helvetica", 16, "bold"))
        self.logo_label.pack(pady=10, padx=10)

        self.export_btn = ctk.CTkButton(self, text="Export uiscript", font=("Helvetica", 16, "bold"), command=self.export_uiscript_signal.emit)
        self.export_btn.pack(pady=(10, 40), padx=10)

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

        self.slot_btn = ctk.CTkButton(self, text="Slot", command=lambda: self.create_widget_signal.emit({"_type": "slot", "width" : 32, "height" : 32}))
        self.slot_btn.pack(pady=10, padx=10)

class SidebarBottom(Sidebar):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.entry_input_signal = Signal(int, int, int, int, int, int, str, list)
        self.create_widgets()

    def __validate_digits(self, string_var):
            value = string_var.get()
            if not value.isdigit():
                string_var.set(''.join(filter(str.isdigit, value)))

    def create_widgets(self):
        def create_labeled_entry(parent, label_text, placeholder=""):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            label = ctk.CTkLabel(frame, text=label_text)
            string_var = tk.StringVar()
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder, textvariable=string_var)
            label.pack(side="left", padx=5)
            entry.pack(side="left", padx=5, expand=True, fill="x")
            frame.pack(side="left", padx=5)
            entry.bind('<KeyRelease>', self.__on_entry_change)
            return frame, entry, string_var

        # Create a frame for entries
        self.entries_frame = ctk.CTkFrame(self)
        self.entries_frame.pack(pady=10, padx=10, fill="x")

        self.entries_frame2 = ctk.CTkFrame(self)
        self.entries_frame2.pack(pady=10, padx=10, fill="x")

        self.x_frame, self.x_entry, self.x_string_var = create_labeled_entry(self.entries_frame, "X:\t")
        self.y_frame, self.y_entry, self.y_string_var = create_labeled_entry(self.entries_frame, "Y:\t")
        self.width_frame, self.width_entry, self.width_string_var = create_labeled_entry(self.entries_frame, "Width:\t")
        self.height_frame, self.height_entry, self.height_string_var = create_labeled_entry(self.entries_frame, "Height:\t")
        self.type_frame, self.type_entry, self.type_string_var = create_labeled_entry(self.entries_frame, "Type:")
        self.parent_frame, self.parent_entry, self.parent_string_var = create_labeled_entry(self.entries_frame, "Parent:")
        self.x_parent_frame, self.x_parent_entry, self.x_parent_string_var = create_labeled_entry(self.entries_frame2, "Parent-X:\t")
        self.y_paren_frame, self.y_parent_entry, self.y_parent_string_var = create_labeled_entry(self.entries_frame2, "Parent-Y:\t")
        self.wdg_name_frame, self.wdg_name_entry, self.wdg_name_string_var = create_labeled_entry(self.entries_frame2, "Name:\t")
        self.style_frame, self.style_entry, self.style_string_var = create_labeled_entry(self.entries_frame2, "Style:\t")
        self.type_entry.configure(state="readonly")
        self.parent_entry.configure(state="readonly")

        self.x_string_var.trace_add("write", lambda *args: self.__validate_digits(self.x_string_var))
        self.y_string_var.trace_add("write", lambda *args: self.__validate_digits(self.y_string_var))
        self.x_parent_string_var.trace_add("write", lambda *args: self.__validate_digits(self.x_parent_string_var))
        self.y_parent_string_var.trace_add("write", lambda *args: self.__validate_digits(self.y_parent_string_var))
        self.width_string_var.trace_add("write", lambda *args: self.__validate_digits(self.width_string_var))
        self.height_string_var.trace_add("write", lambda *args: self.__validate_digits(self.height_string_var))

    def set_entry_values(self, x, y, x_parent, y_parent, width, height, type, parent, wdg_name, style):
        self.type_entry.configure(state="normal")
        self.parent_entry.configure(state="normal")

        self.insert_entry_text(self.x_entry, x)
        self.insert_entry_text(self.y_entry, y)
        self.insert_entry_text(self.x_parent_entry, x_parent)
        self.insert_entry_text(self.y_parent_entry, y_parent)
        self.insert_entry_text(self.width_entry, width)
        self.insert_entry_text(self.height_entry, height)
        self.insert_entry_text(self.type_entry, type)
        self.insert_entry_text(self.parent_entry, parent)
        self.insert_entry_text(self.wdg_name_entry, wdg_name)
        self.insert_entry_text(self.style_entry, style)

        self.type_entry.configure(state="readonly")
        self.parent_entry.configure(state="readonly")

    def __on_entry_change(self, event):
        x = self.x_entry.get()
        y = self.y_entry.get()
        x_parent = self.x_parent_entry.get()
        y_parent = self.y_parent_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()
        wdg_name = self.wdg_name_entry.get()
        style = self.style_entry.get()
        # type = self.type_entry.get()
        # parent = self.parent_entry.get()
        try:
            int(x), int(y), int(x_parent), int(y_parent), int(width), int(height), str(wdg_name), [opt.strip() for opt in list(style.split(","))]
        except:
            pass
        else:
            self.entry_input_signal.emit(int(x), int(y), int(x_parent), int(y_parent), int(width), int(height), str(wdg_name), [opt.strip() for opt in list(style.split(","))])