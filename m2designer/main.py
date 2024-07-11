import customtkinter
from components.draggableLabel import DraggableLabel
from components.mainWindow import MainWindowLabel

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("2000x500")

# def button_function():
#     print("button pressed")

# Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

# label = DraggableLabel(master=app, text="test", parent_width_callback=app.winfo_width, parent_height_callback=app.winfo_height, width=400, height=400)
# label.place(x=30, y=10, anchor=customtkinter.CENTER)

mainLabel = MainWindowLabel(master=app, text="main", parent_width_callback=app.winfo_width, parent_height_callback=app.winfo_height, width=400, height=400)
mainLabel.place(x=30, y=10, anchor=customtkinter.CENTER)

mainLabel2 = MainWindowLabel(master=app, text="main", parent_width_callback=app.winfo_width, parent_height_callback=app.winfo_height, width=100, height=400)
mainLabel2.place(x=30, y=10, anchor=customtkinter.CENTER)

l = customtkinter.CTkLabel(master=app, image="")

app.mainloop()