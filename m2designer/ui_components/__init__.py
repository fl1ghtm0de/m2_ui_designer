import customtkinter as ctk
import tkinter as tk

class DropdownWithCheckboxes(ctk.CTkFrame):
    def __init__(self, master, options, width, height, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.selected_options = ctk.StringVar(value="Select Options")

        # Create the button that looks like a default CTkButton
        self.button = ctk.CTkButton(self, textvariable=self.selected_options, width=width, height=height, command=self.toggle_menu)
        self.button.pack(fill='x', padx=10, pady=10)

        self.options_frame = ctk.CTkFrame(self)
        self.check_vars = []
        for option in options:
            var = ctk.StringVar(value="off")
            checkbox = ctk.CTkCheckBox(self.options_frame, text=option, variable=var, onvalue="on", offvalue="off")
            checkbox.pack(anchor='w')
            self.check_vars.append(var)

        self.options_frame.pack_forget()

    def toggle_menu(self):
        if self.options_frame.winfo_ismapped():
            self.options_frame.pack_forget()
        else:
            self.options_frame.pack(pady=10)
            self.update_button_text()

    def update_button_text(self):
        selected_options = [checkbox.cget("text") for checkbox, var in zip(self.options_frame.winfo_children(), self.check_vars) if var.get() == "on"]
        if selected_options:
            self.selected_options.set(", ".join(selected_options))
        else:
            self.selected_options.set("Select Options")