import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from ctk_signal import Signal

class Sidebar(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widget_signal = Signal(dict)
        self.show_error_signal = Signal(str, str)
        self.configure(width=200, corner_radius=0)
        self.set_styles()
        ctk.set_appearance_mode("System")  # Set the appearance mode to follow the system setting
        ctk.AppearanceModeTracker.add(self.change_appearance_mode)  # Track appearance mode changes

    def insert_entry_text(self, entry:ctk.CTkEntry, text):
        if not isinstance(text, str):
            text = str(text)

        entry.delete(0, ctk.END)
        entry.insert(0, text)

    def set_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        current_mode = ctk.get_appearance_mode()

        if current_mode == "Dark":
            treeview_bg = "#2B2B2B"
            treeview_fg = "white"
            treeview_field_bg = "#2B2B2B"
            heading_bg = "#1F6AA5"  # Light blue to match CustomTkinter button
            heading_fg = "white"
            active_bg = "#144870"   # Slightly lighter blue
            selected_bg = "#555555"
        else:  # Light mode
            treeview_bg = "#ffffff"
            treeview_fg = "black"
            treeview_field_bg = "#ffffff"
            heading_bg = "#1F6AA5"  # Light blue to match CustomTkinter button
            heading_fg = "white"
            active_bg = "#144870"   # Slightly lighter blue
            selected_bg = "#cccccc"

        style.configure("Treeview",
                        background=treeview_bg,
                        foreground=treeview_fg,
                        fieldbackground=treeview_field_bg,
                        rowheight=25,
                        font=("Arial", 12),
                        borderwidth=0,
                        )

        style.configure("Treeview.Heading",
                        background=heading_bg,
                        foreground=heading_fg,
                        relief="raised",
                        padding=(10, 5),
                        font=("Arial", 12, "bold"),
                        borderwidth=0,
                        )

        # style.configure('Edge.Treeview', highlightthickness=0, bd=0)

        style.map("Treeview.Heading",
                background=[('active', active_bg), ('pressed', heading_bg)],
                relief=[('pressed', 'sunken')])

        style.map("Treeview",
                background=[('selected', selected_bg)],
                foreground=[('selected', 'white')])

    def change_appearance_mode(self, new_appearance_mode):
        self.set_styles()
        # Update treeview widgets in the application to apply new styles
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.configure(style='Treeview')

class SidebarRight(Sidebar):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()
        self.entry_input_signal = Signal(object, object)
        self.attr_type_map = {}

    def create_widgets(self):
        self.attribute_table = ttk.Treeview(self, columns=("Attribute", "Value"), show='headings')
        self.attribute_table.heading("Attribute", text="Attribute")
        self.attribute_table.heading("Value", text="Value")
        self.attribute_table.bind('<Double-1>', self.on_double_click)

        self.attribute_table.pack(expand=True, fill='both')

    def add_row(self, attribute, value):
        self.attribute_table.insert("", "end", values=(attribute, value))

    def clear_table(self):
        for item in self.attribute_table.get_children():
            self.attribute_table.delete(item)

    def set_entry_values(self, data):
        self.clear_table()
        for widget_attr, attr_value in data.items():
            self.attr_type_map[widget_attr] = type(attr_value)
            self.add_row(widget_attr, attr_value)

    def on_double_click(self, event):
        item_id = self.attribute_table.identify_row(event.y)
        column = self.attribute_table.identify_column(event.x)

        if column == '#2':  # Make sure the click is on the "Value" column
            self.edit_value_cell(item_id)

    def edit_value_cell(self, item_id):
        x, y, width, height = self.attribute_table.bbox(item_id, 'Value')
        key, value = self.attribute_table.item(item_id, 'values')

        self.entry_popup = tk.Entry(self)
        self.entry_popup.configure(highlightthickness=0, bd=0)
        self.entry_popup.insert(0, value)
        self.entry_popup.focus()
        self.entry_popup.place(
            x=x + self.attribute_table.winfo_rootx() - self.winfo_rootx(),
            y=y + self.attribute_table.winfo_rooty() - self.winfo_rooty(),
            width=width,
            height=height
        )
        self.entry_popup.bind('<Return>', lambda event: self.update_value(item_id))
        self.entry_popup.bind('<FocusOut>', lambda event: self.destroy_entry_popup())

    def update_value(self, item_id):
        try:
            new_value = self.entry_popup.get()
            current_values = list(self.attribute_table.item(item_id, 'values'))
            old_value = current_values[1]
            current_values[1] = new_value
            try:
                self.attr_type_map[current_values[0]](current_values[1]) # try to cast the current input to the initial datatype
            except ValueError:
                self.show_error_signal.emit("Invalid input", f"Exspected type: {self.attr_type_map[current_values[0]]}")
                return
            else:
                success = self.entry_input_signal.emit(current_values[0], self.attr_type_map[current_values[0]](current_values[1])) # if cast succeeds, emit the new data

            if success:
                self.attribute_table.item(item_id, values=current_values)

        except Exception as e:
            print(f"Error updating value: {e}")
        finally:
            self.entry_popup.forget()

    def destroy_entry_popup(self):
        if self.entry_popup:
            self.entry_popup.destroy()
            self.entry_popup = None


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

        self.slot_btn = ctk.CTkButton(self, text="Slot", command=lambda: self.create_widget_signal.emit({"_type": "slot"}))
        self.slot_btn.pack(pady=10, padx=10)

        self.text_btn = ctk.CTkButton(self, text="Text", command=lambda: self.create_widget_signal.emit({"_type": "text", "width" : 50, "height" : 20}))
        self.text_btn.pack(pady=10, padx=10)

        self.image_btn = ctk.CTkButton(self, text="Image", command=lambda: self.create_widget_signal.emit({"_type": "image"}))
        self.image_btn.pack(pady=10, padx=10)

        self.titlebar_btn = ctk.CTkButton(self, text="Titlebar", command=lambda: self.create_widget_signal.emit({"_type": "titlebar", "width": 230, "height": 30}))
        self.titlebar_btn.pack(pady=10, padx=10)

# class SidebarBottom(Sidebar):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)
#         self.entry_input_signal = Signal(int, int, int, int, int, int, str, list, str)
#         self.create_widgets()

#     def __validate_digits(self, string_var):
#             value = string_var.get()
#             if not value.isdigit():
#                 string_var.set(''.join(filter(str.isdigit, value)))

#     def create_widgets(self):
#         def create_labeled_entry(parent, label_text, placeholder=""):
#             frame = ctk.CTkFrame(parent, fg_color="transparent")
#             label = ctk.CTkLabel(frame, text=label_text)
#             string_var = tk.StringVar()
#             entry = ctk.CTkEntry(frame, placeholder_text=placeholder, textvariable=string_var)
#             label.pack(side="left", padx=5)
#             entry.pack(side="left", padx=5, expand=True, fill="x")
#             frame.pack(side="left", padx=5)
#             entry.bind('<KeyRelease>', self.__on_entry_change)
#             return frame, entry, string_var, label

#         # Create a frame for entries
#         self.entries_frame = ctk.CTkFrame(self)
#         self.entries_frame.pack(pady=10, padx=10, fill="x")

#         self.entries_frame2 = ctk.CTkFrame(self)
#         self.entries_frame2.pack(pady=10, padx=10, fill="x")

#         self.x_frame, self.x_entry, self.x_string_var, self.x_label = create_labeled_entry(self.entries_frame, "X:\t")
#         self.y_frame, self.y_entry, self.y_string_var, self.y_label = create_labeled_entry(self.entries_frame, "Y:\t")
#         self.width_frame, self.width_entry, self.width_string_var, self.y_label = create_labeled_entry(self.entries_frame, "Width:\t")
#         self.height_frame, self.height_entry, self.height_string_var, self.height_label = create_labeled_entry(self.entries_frame, "Height:\t")
#         self.type_frame, self.type_entry, self.type_string_var, self.type_label = create_labeled_entry(self.entries_frame, "Type:")
#         self.parent_frame, self.parent_entry, self.parent_string_var, self.parent_label = create_labeled_entry(self.entries_frame, "Parent:")
#         self.x_parent_frame, self.x_parent_entry, self.x_parent_string_var, self.x_parent_label = create_labeled_entry(self.entries_frame2, "Parent-X:\t")
#         self.y_parent_frame, self.y_parent_entry, self.y_parent_string_var, self.y_parent_label = create_labeled_entry(self.entries_frame2, "Parent-Y:\t")
#         self.wdg_name_frame, self.wdg_name_entry, self.wdg_name_string_var, self.wdg_name_label = create_labeled_entry(self.entries_frame2, "Name:\t")
#         self.style_frame, self.style_entry, self.style_string_var, self.style_label = create_labeled_entry(self.entries_frame2, "Style:\t")
#         self.text_frame, self.text_entry, self.text_string_var, self.text_label = create_labeled_entry(self.entries_frame2, "Text:")
#         self.type_entry.configure(state="readonly")
#         self.parent_entry.configure(state="readonly")

#         self.x_string_var.trace_add("write", lambda *args: self.__validate_digits(self.x_string_var))
#         self.y_string_var.trace_add("write", lambda *args: self.__validate_digits(self.y_string_var))
#         self.x_parent_string_var.trace_add("write", lambda *args: self.__validate_digits(self.x_parent_string_var))
#         self.y_parent_string_var.trace_add("write", lambda *args: self.__validate_digits(self.y_parent_string_var))
#         self.width_string_var.trace_add("write", lambda *args: self.__validate_digits(self.width_string_var))
#         self.height_string_var.trace_add("write", lambda *args: self.__validate_digits(self.height_string_var))

#     def set_entry_values(self, x, y, x_parent, y_parent, width, height, type, parent, wdg_name, style, text):
#         self.type_entry.configure(state="normal")
#         self.parent_entry.configure(state="normal")

#         self.insert_entry_text(self.x_entry, x)
#         self.insert_entry_text(self.y_entry, y)
#         self.insert_entry_text(self.x_parent_entry, x_parent)
#         self.insert_entry_text(self.y_parent_entry, y_parent)
#         self.insert_entry_text(self.width_entry, width)
#         self.insert_entry_text(self.height_entry, height)
#         self.insert_entry_text(self.type_entry, type)
#         self.insert_entry_text(self.parent_entry, parent)
#         self.insert_entry_text(self.wdg_name_entry, wdg_name)
#         self.insert_entry_text(self.style_entry, style)

#         if text == "None":
#             self.text_label.pack_forget()
#             self.text_entry.pack_forget()
#         else:
#             self.text_label.pack(side="left", padx=5, expand=True, fill="x")
#             self.text_entry.pack(side="left", padx=5, expand=True, fill="x")
#         self.insert_entry_text(self.text_entry, text)

#         self.type_entry.configure(state="readonly")
#         self.parent_entry.configure(state="readonly")

#     def __on_entry_change(self, event):
#         x = self.x_entry.get()
#         y = self.y_entry.get()
#         x_parent = self.x_parent_entry.get()
#         y_parent = self.y_parent_entry.get()
#         width = self.width_entry.get()
#         height = self.height_entry.get(
#         wdg_name = self.wdg_name_entry.get()
#         style = self.style_entry.get()
#         text = self.text_entry.get()
#         try:
#             int(x), int(y), int(x_parent), int(y_parent), int(width), int(height), str(wdg_name), [opt.strip() for opt in list(style.split(","))], str(text)
#         except:
#             pass
#         else:
#             self.entry_input_signal.emit(int(x), int(y), int(x_parent), int(y_parent), int(width), int(height), str(wdg_name), [opt.strip() for opt in list(style.split(","))], str(text))