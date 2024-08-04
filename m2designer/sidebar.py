import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from ctk_signal import Signal
from config_loader import Config

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
        self.current_mode = ctk.get_appearance_mode()

        if self.current_mode == "Dark":
            self.treeview_bg = "#2B2B2B"
            self.treeview_fg = "white"
            self.treeview_field_bg = "#2B2B2B"
            self.heading_bg = "#1F6AA5"  # Light blue to match CustomTkinter button
            self.heading_fg = "white"
            self.active_bg = "#144870"  # Slightly lighter blue
            self.selected_bg = "#555555"
            self.entry_bg = "#2B2B2B"
            self.entry_fg = "white"
        else:  # Light mode
            self.treeview_bg = "#ffffff"
            self.treeview_fg = "black"
            self.treeview_field_bg = "#ffffff"
            self.heading_bg = "#1F6AA5"  # Light blue to match CustomTkinter button
            self.heading_fg = "white"
            self.active_bg = "#144870"  # Slightly lighter blue
            self.selected_bg = "#cccccc"
            self.entry_bg = "#ffffff"
            self.entry_fg = "black"

        style.configure("Treeview",
                        background=self.treeview_bg,
                        foreground=self.treeview_fg,
                        fieldbackground=self.treeview_field_bg,
                        rowheight=25,
                        font=("Arial", 12),
                        borderwidth=0,
                        )

        style.configure("Treeview.Heading",
                        background=self.heading_bg,
                        foreground=self.heading_fg,
                        relief="raised",
                        padding=(10, 5),
                        font=("Arial", 12, "bold"),
                        borderwidth=0,
                        )

        style.map("Treeview.Heading",
                background=[('active', self.active_bg), ('pressed', self.heading_bg)],
                relief=[('pressed', 'sunken')])

        style.map("Treeview",
                background=[('selected', self.selected_bg)],
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
        self.cfg_loader = Config()
        self.dropdown_selection = {}
        self.entry_popup = None
        self.dropdown_popup = {}

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
        self.dropdown_selection.clear()
        self.destroy_entry_popup()

    def set_entry_values(self, data):
        self.clear_table()
        for widget_attr, attr_value in data.items():
                self.attr_type_map[widget_attr] = type(attr_value)
                if widget_attr in self.cfg_loader.dropdown_attributes:
                    self.add_row(widget_attr, "")
                    self.dropdown_selection[widget_attr] = attr_value
                    self.update_idletasks()  # Ensure the row is fully added and visible
                    item_id = self.attribute_table.get_children()[-1]  # Get the last added row item id
                    self.edit_value_cell(item_id)  # Automatically apply the popup menu
                else:
                    self.add_row(widget_attr, attr_value)

    def on_double_click(self, event):
        item_id = self.attribute_table.identify_row(event.y)
        column = self.attribute_table.identify_column(event.x)

        if column == '#2':  # Make sure the click is on the "Value" column
            self.edit_value_cell(item_id)

    def on_item_selected(self, attr, value, key, y_offset):
        success = self.entry_input_signal.emit(attr, value)
        self.dropdown_popup[key].menu.post(self.dropdown_popup[key].winfo_rootx(), self.dropdown_popup[key].winfo_rooty() + y_offset) # automatically re-open the menu at the same position

    def edit_value_cell(self, item_id):
        x, y, width, height = self.attribute_table.bbox(item_id, 'Value')
        key, value = self.attribute_table.item(item_id, 'values')

        if key in self.cfg_loader.dropdown_attributes:
            self.dropdown_popup[key] = tk.Menubutton(self, text="click to select", relief=ctk.RAISED, anchor='w')
            self.dropdown_popup[key].place(
                x=x + self.attribute_table.winfo_rootx() - self.winfo_rootx(),
                y=y + self.attribute_table.winfo_rooty() - self.winfo_rooty(),
                width=width - 4,
                height=height
            )
            self.dropdown_popup[key].menu = tk.Menu(self.dropdown_popup[key], tearoff=0)
            self.dropdown_popup[key]["menu"] = self.dropdown_popup[key].menu

            for option in getattr(self.cfg_loader, f"{key}_options"):
                item = tk.IntVar()
                if key in self.dropdown_selection.keys():
                    if option in self.dropdown_selection[key]:
                        item.set(1)
                    else:
                        item.set(0)

                self.dropdown_popup[key].menu.add_checkbutton(
                    label=option,
                    variable=item,
                    command=lambda opt=option, var=item: self.on_item_selected(key, opt, key, height)
                )

            self.dropdown_popup[key].configure(highlightthickness=0, bd=0,
                                    background=self.entry_bg,
                                    foreground=self.entry_fg,
                                    activebackground=self.entry_bg,
                                    activeforeground=self.entry_fg,
                                    font=("Arial", 12))
            self.dropdown_popup[key].bind('<FocusOut>', lambda event: self.destroy_entry_popup())

        else:
            self.entry_popup_text_var = tk.StringVar()
            self.entry_popup = tk.Entry(self, textvariable=self.entry_popup_text_var)
            self.entry_popup.insert(0, value)
            self.entry_popup.focus()
            self.entry_popup.place(
                x=x + self.attribute_table.winfo_rootx() - self.winfo_rootx() + 3, # small offset to match placing
                y=y + self.attribute_table.winfo_rooty() - self.winfo_rooty(),
                width=width - 4, # small offset to match placing
                height=height
            )
            self.entry_popup.configure(highlightthickness=0, bd=0,
                                    background=self.entry_bg,
                                    foreground=self.entry_fg,
                                    font=("Arial", 12))
            self.entry_popup_text_var.trace_add("write", lambda *args: self.update_value(item_id)) # update values on input

    def update_value(self, item_id):
        try:
            new_value = self.entry_popup_text_var.get()
            current_values = list(self.attribute_table.item(item_id, 'values'))
            old_value = current_values[1]
            current_values[1] = new_value

            try:
                self.attr_type_map[current_values[0]](current_values[1]) # try to cast the current input to the initial datatype
            except ValueError:
                self.show_error_signal.emit("Invalid input", f"Exspected type: {self.attr_type_map[current_values[0]]}")
                return
            else: # if cast succeeds, emit the new data
                success = self.entry_input_signal.emit(current_values[0], self.attr_type_map[current_values[0]](current_values[1]))

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

        self.text_btn = ctk.CTkButton(self, text="Text", command=lambda: self.create_widget_signal.emit({"_type": "text", "width" : 90, "height" : 8}))
        self.text_btn.pack(pady=10, padx=10)

        self.image_btn = ctk.CTkButton(self, text="Image", command=lambda: self.create_widget_signal.emit({"_type": "image"}))
        self.image_btn.pack(pady=10, padx=10)

        self.titlebar_btn = ctk.CTkButton(self, text="Titlebar", command=lambda: self.create_widget_signal.emit({"_type": "titlebar", "width": 230, "height": 23}))
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