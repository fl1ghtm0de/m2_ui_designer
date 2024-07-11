from components.draggableLabel import DraggableLabel
from tools.tilteImage import create_tiled_image, add_borders, make_final_image

class MainWindowLabel(DraggableLabel):
    def __init__(self, *args, **kwargs):
        width = kwargs.pop("width", 0)
        height = kwargs.pop("height", 0)
        til_img = create_tiled_image(r"C:\Users\vital\Projects\m2_ui_designer\m2designer\images\board\board_base.png", width, height)
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
        super().__init__(image=til_img, width=width, height=height, *args, **kwargs)
