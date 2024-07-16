from components.base_widget import BaseWidget
from tools.image_tools import stretch_image
from tkinter import Canvas
from config_loader import Config

class Thinboard(BaseWidget):
    def __init__(self, canvas, *args, **kwargs):
        width = kwargs.pop("width", 0)
        height = kwargs.pop("height", 0)
        cfg_loader = Config()
        self.stretch_img = stretch_image(cfg_loader.thinboard, width, height, 3)
        super().__init__(canvas=canvas, width=width, height=height, image=self.stretch_img, image_path=cfg_loader.thinboard, resizable=True, *args, **kwargs)
        # self.resize_type = "tile"

    def __str__(self):
        return f"thinboard"