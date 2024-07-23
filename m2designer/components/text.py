from components.base_widget import BaseWidget
from tools.image_tools import create_empty_image

class Text(BaseWidget):
    def __init__(self, canvas, *args, **kwargs):
        width = kwargs.pop("width", 0)
        height = kwargs.pop("height", 0)
        self.empty_img = create_empty_image(width, height)
        super().__init__(canvas=canvas, width=width, height=height, image=self.empty_img, text="a placeholder text", resizable=False, *args, **kwargs)
        # self.resize_type = "tile"

    def __str__(self):
        return f"text"

    def get_data(self):
        data = super().get_data()
        del data["image_path"]
        data["text"] = self.text
        return data