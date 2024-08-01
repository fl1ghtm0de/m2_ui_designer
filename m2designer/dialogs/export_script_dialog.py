import customtkinter as ctk
import tkinter as tk
from config_loader import Config

class UiscriptExportDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Imports"):

        super().__init__(parent)
        self.title(title)

        self.dropdown_menu = tk.Menubutton(self, text="Additional imports", relief=ctk.RAISED, anchor='w')
        self.dropdown_menu.pack(pady=10, padx=10)

        self.dropdown_menu.menu = tk.Menu(self.dropdown_menu, tearoff=0)
        self.dropdown_menu["menu"] = self.dropdown_menu.menu

        self.submit_button = ctk.CTkButton(self, text="Generate", command=self.on_submit)
        self.submit_button.pack(pady=10, padx=10)

        for import_option in Config().uiscript_imports:
            item = tk.IntVar()
            self.dropdown_menu.menu.add_checkbutton(
                label=import_option,
                variable=item,
                command=lambda opt=import_option, var=item: self.on_item_selected(opt, 25)
            )

        self.grab_set() # disable parent window while dialog is shown
        self.transient(parent) # make dialog always stay on top of parent

        self.result = []

    def on_item_selected(self, value, y_offset):
        # success = self.entry_input_signal.emit(attr, value)
        if value in self.result:
            self.result.remove(value)
        else:
            self.result.append(value)
        self.dropdown_menu.menu.post(self.dropdown_menu.winfo_rootx(), self.dropdown_menu.winfo_rooty() + y_offset) # automatically re-open the menu at the same position

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