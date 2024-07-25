import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkFont

class Dropdown(ctk.CTkButton):
    def __init__(self, master, options, button_width, button_height, menu_width=None, *args, **kwargs):
        super().__init__(master, command=self.toggle_menu, width=button_width, height=button_height, *args, **kwargs)
        self.menu_visible = False

        # Determine the width of the options frame
        if menu_width is None:
            menu_width = self.calculate_text_width(options) + 80  # Add some padding

        # Create options frame with appropriate width
        self.options_frame = ctk.CTkFrame(master, width=menu_width)
        self.check_vars = []
        self.checkboxes = []
        for option in options:
            var = ctk.StringVar(value="off")
            checkbox = ctk.CTkCheckBox(self.options_frame, text=option, variable=var, onvalue="on", offvalue="off", width=menu_width)
            checkbox.pack(anchor='w', pady=2)
            self.check_vars.append(var)
            self.checkboxes.append((option, var))

        self.options_frame.pack_forget()

    def toggle_menu(self):
        if self.menu_visible:
            self.options_frame.place_forget()
        else:
            self.options_frame.place(in_=self, relx=0, rely=1, anchor='nw')
            self.options_frame.lift()
        self.menu_visible = not self.menu_visible

    def calculate_text_width(self, options):
        # Create a font object to measure the text width
        font = tkFont.Font(family="Helvetica", size=12)
        max_width = 0
        for option in options:
            width = font.measure(option)
            if width > max_width:
                max_width = width
        return max_width

    def get_checked_options(self):
        checked_options = [option for option, var in self.checkboxes if var.get() == "on"]
        return checked_options