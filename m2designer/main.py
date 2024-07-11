import customtkinter
from components.draggableLabel import DraggableLabel
from tools.tiltedImage import create_tilted_image, add_borders, make_final_image

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("2000x500")

# def button_function():
#     print("button pressed")

# Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

til_img = create_tilted_image(r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board\board_base.png", 800, 400)
til_img = add_borders(
                        til_img,
                        border_images={
                            "top" : r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board_2\board_line_top.png",
                            "left": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board_2\board_line_left.png",
                            "bottom": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board_2\board_line_bottom.png",
                            "right": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board_2\board_line_right.png",
                            "top_left_corner": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board_2\board_corner_lefttop.png",
                            "bottom_left_corner": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board_2\board_corner_leftbottom.png",
                            "bottom_right_corner": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board_2\board_corner_rightbottom.png",
                            "top_right_corner": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board_2\board_corner_righttop.png",
                            "close_button": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\button\close_button.png",
                            "minimize_button": r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\button\minimize_button.png"
                        },
                    )

til_img = make_final_image(til_img)

label = DraggableLabel(master=app, text="test", image=til_img ,parent_width_callback=app.winfo_width, parent_height_callback=app.winfo_height, width=400, height=400)
label.place(x=30, y=10, anchor=customtkinter.CENTER)

l = customtkinter.CTkLabel(master=app, image="")

app.mainloop()