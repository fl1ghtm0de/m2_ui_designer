from components.base_widget import BaseWidget
from PIL import Image, ImageTk
from config_loader import Config
from tools.image_tools import stretch_image

class Button(BaseWidget):
    sizeMapping = {
        "big" : (51, 37),
        "large" : (88, 21),
        "middle" : (61, 21),
        "small" : (43, 21),
        "small_thin" : (60, 20),
        "xlarge" : (180, 25),
        "xlarge_thin" : (57, 30),
        "xsmall" : (37, 19)
    }

    def __init__(self, canvas, button_type, *args, **kwargs):
        self.button_type = button_type.lower()
        width = Button.sizeMapping.get(button_type, (0, 0))[0]
        height = Button.sizeMapping.get(button_type, (0, 0))[1]
        cfg_loader = Config()
        img_path = cfg_loader.construct_path(cfg_loader.BUTTON_PATH, f"{self.button_type}_button.png")
        self.stretch_img = stretch_image(img_path, width, height, 3)
        super().__init__(canvas=canvas, image=self.stretch_img, image_path=img_path, width=width, height=height, text="", *args, **kwargs)

    def __str__(self):
        return f"button_{self.button_type}"

    def get_data(self):
        data = super().get_data()
        data["button_type"] = self.button_type
        return data