from components.base_widget import BaseWidget
from tools.image_tools import summarize_images_side_by_side
from tkinter import Canvas
from config_loader import Config

class RadioButton(BaseWidget):
    def __init__(self, canvas, *args, **kwargs):
        width = kwargs.pop("width", 0)
        height = kwargs.pop("height", 0)
        self.button_count = kwargs.pop("button_count", 0)
        self.button_image_paths = kwargs.pop("button_image_paths", [])
        cfg_loader = Config()
        self.summed_image = summarize_images_side_by_side(*self.button_image_paths)
        super().__init__(canvas=canvas, width=width, height=height, image=self.summed_image, image_path=cfg_loader.thinboard, resizable=True, *args, **kwargs)
        # self.resize_type = "tile"

    def __str__(self):
        return f"radiobutton"

    def get_data(self):
        data = super().get_data()
        data["button_count"] = self.button_count
        for i, img in enumerate(self.button_images):
            data[f"Image {i}"] = img
        return data