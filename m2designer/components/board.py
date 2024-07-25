from components.base_widget import BaseWidget
from components.titlebar import Titlebar
from tools.image_tools import create_tiled_image, add_borders, make_final_image
from tkinter import Canvas
from config_loader import Config
class Board(BaseWidget):
    def __init__(self, canvas, *args, **kwargs):
        width = kwargs.pop("width", 0)
        height = kwargs.pop("height", 0)
        cfg_loader = Config()
        til_img = create_tiled_image(cfg_loader.board_base, width, height)
        til_img = add_borders(til_img)

        self.til_img = make_final_image(til_img)
        super().__init__(canvas=canvas, width=width, height=height, image=self.til_img, image_path=cfg_loader.board_base, resizable=True, *args, **kwargs)
        # self.resize_type = "tile"

    def __str__(self):
        return f"board"

    def get_data(self):
        data = super().get_data()
        del data["image_path"]
        return data

    # def create_context_menu(self):
    #     super().create_context_menu()
    #     self.context_menu.insert_command(8, label="Add Titlebar", command=self.add_titlebar)
    #     self.context_menu.insert_separator(8)