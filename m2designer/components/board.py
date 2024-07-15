from components.draggableLabel import DraggableLabel
from tools.image_tools import create_tiled_image, add_borders, make_final_image
from tkinter import Canvas
from ConfigLoader import Config
class Board(DraggableLabel):
    def __init__(self, canvas, *args, **kwargs):
        width = kwargs.pop("width", 0)
        height = kwargs.pop("height", 0)
        cfg_loader = Config()
        til_img = create_tiled_image(cfg_loader.board_base, width, height)
        border_images = {
                                    "top" : cfg_loader.top,
                                    "left": cfg_loader.left,
                                    "bottom": cfg_loader.bottom,
                                    "right": cfg_loader.right,
                                    "top_left_corner": cfg_loader.top_left_corner,
                                    "bottom_left_corner": cfg_loader.bottom_left_corner,
                                    "bottom_right_corner": cfg_loader.bottom_right_corner,
                                    "top_right_corner": cfg_loader.top_right_corner,
                                    "close_button": cfg_loader.close_button,
                                    "minimize_button": cfg_loader.minimize_button
                                }
        til_img = add_borders(
                                til_img,
                                border_images
                            )

        self.til_img = make_final_image(til_img)
        super().__init__(canvas=canvas, width=width, height=height, image=self.til_img, image_path=cfg_loader.board_base, image_borders=border_images, resizable=True, *args, **kwargs)
        # self.resize_type = "tile"

    def __str__(self):
        return f"board"