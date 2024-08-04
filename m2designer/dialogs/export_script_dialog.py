import customtkinter as ctk
import tkinter as tk
# import encodings.aliases
from config_loader import Config

class UiscriptExportDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Imports"):

        super().__init__(parent)
        self.title(title)
        self.cfg_loader = Config()
        self.dropdown_menu = tk.Menubutton(self, text="Additional imports", relief=ctk.RAISED, anchor='w')
        self.dropdown_menu.pack(pady=10, padx=10)

        self.dropdown_menu.menu = tk.Menu(self.dropdown_menu, tearoff=0)
        self.dropdown_menu["menu"] = self.dropdown_menu.menu

        self.file_name_text_var = ctk.StringVar(value="Enter filename")
        self.file_name_entry = ctk.CTkEntry(self, textvariable=self.file_name_text_var)
        self.file_name_text_var.trace_add("write", lambda *args: self.on_filename_input(self.file_name_text_var.get())) # update values on input
        self.file_name_entry.bind("<FocusIn>", self.foc_in)
        self.file_name_entry.pack(pady=10, padx=10)

        # self.dropdown_encoding_menu = tk.Menubutton(self, text="File encoding", relief=ctk.RAISED, anchor='w')
        # self.dropdown_encoding_menu.pack(pady=10, padx=10)

        # self.dropdown_encoding_menu.menu = tk.Menu(self.dropdown_encoding_menu, tearoff=0)
        # self.dropdown_encoding_menu["menu"] = self.dropdown_encoding_menu.menu

        self.submit_button = ctk.CTkButton(self, text="Generate", command=self.on_submit)
        self.submit_button.pack(pady=10, padx=10)

        for import_option in self.cfg_loader.uiscript_imports:
            item = tk.IntVar()
            self.dropdown_menu.menu.add_checkbutton(
                label=import_option,
                variable=item,
                command=lambda opt=import_option, var=item: self.on_item_selected(self.dropdown_menu, opt, 25)
            )

        # self.aliases = encodings.aliases.aliases # use this if u want to see all available encodings according to ur version of python
        # self.all_encodings = set(self.aliases.values())
        # self.all_encodings = self.cfg_loader.encodings
        # for encoding_option in sorted(self.all_encodings):
        #     item = tk.IntVar()
        #     self.dropdown_encoding_menu.menu.add_checkbutton(
        #         label=encoding_option,
        #         variable=item,
        #         command=lambda opt=encoding_option, var=item: self.on_item_selected(self.dropdown_encoding_menu, opt, 25)
        #     )


        self.grab_set() # disable parent window while dialog is shown
        self.transient(parent) # make dialog always stay on top of parent

        self.result = []
        self.filename = "uiscript.py"

    def foc_in(self, event):
        if self.file_name_text_var.get() == "Enter filename":
            self.file_name_entry.delete('0', 'end')

    def on_filename_input(self, text):
        if not text.endswith(".py"):
            text = f"{text}.py"
        self.filename = text

    def on_item_selected(self, parent, value, y_offset):
        # success = self.entry_input_signal.emit(attr, value)
        if value in self.result:
            self.result.remove(value)
        else:
            self.result.append(value)
        parent.menu.post(parent.winfo_rootx(), parent.winfo_rooty() + y_offset) # automatically re-open the menu at the same position

    def on_submit(self):
        self.destroy()


            # self.dropdown_popup[key] = tk.Menubutton(self, text="click to select", relief=ctk.RAISED, anchor='w')
            # self.dropdown_popup[key].place(
            #     x=x + self.attribute_table.winfo_rootx() - self.winfo_rootx(), # small offset to match placing
            #     y=y + self.attribute_table.winfo_rooty() - self.winfo_rooty(),
            #     width=width - 4,
            #     height=height
            # )
            # self.dropdown_popup[key].menu = tk.Menu(self.dropdown_popup[key], tearoff=0)
            # self.dropdown_popup[key]["menu"] = self.dropdown_popup[key].menu

            # for option in getattr(self.cfg_loader, f"{key}_options"):
            #     item = tk.IntVar()
            #     if key in self.dropdown_selection.keys():
            #         if option in self.dropdown_selection[key]:
            #             item.set(1)
            #         else:
            #             item.set(0)

            #     self.dropdown_popup[key].menu.add_checkbutton(
            #         label=option,
            #         variable=item,
            #         command=lambda opt=option, var=item: self.on_item_selected(key, opt, key, height)
            #     )