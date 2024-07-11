import customtkinter
from components.draggableItem import DraggableLabel

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

# def button_function():
#     print("button pressed")

# Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

label = DraggableLabel(master=app, text="test")
label.place(x=0, y=0, anchor=customtkinter.CENTER)


app.mainloop()