from components.base_widget import BaseWidget
from tools.image_tools import create_titlebar
from config_loader import Config

class Titlebar(BaseWidget):
    def __init__(self, canvas, *args, **kwargs):
        width = kwargs.pop("width", 0)
        height = kwargs.pop("height", 0)
        cfg_loader = Config()
        self.bar_img = create_titlebar(cfg_loader.titlebar_left, cfg_loader.titlebar_center, cfg_loader.titlebar_right, width)
        super().__init__(canvas=canvas, width=width, height=height, image=self.bar_img, text="", resizable=False, *args, **kwargs)

    def __str__(self):
        return f"titlebar"

    def get_data(self):
        data = super().get_data()
        del data["image_path"]
        data["text"] = self.text
        return data

    def create_context_menu(self): ...