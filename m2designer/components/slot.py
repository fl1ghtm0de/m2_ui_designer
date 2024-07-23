from components.base_widget import BaseWidget
from tools.image_tools import create_tiled_image, make_final_image, get_image_size
from config_loader import Config

class Slot(BaseWidget):
    def __init__(self, canvas, *args, **kwargs):
        cfg_loader = Config()
        width, height = get_image_size(cfg_loader.slot)
        self.slot_count = kwargs.pop("slot_count", 1)
        self.slot_img = make_final_image(create_tiled_image(cfg_loader.slot, width, height * self.slot_count))
        super().__init__(canvas=canvas, width=width, height=height, image=self.slot_img, image_path=cfg_loader.slot, resizable=False, *args, **kwargs)

    def __str__(self):
        return f"Slot"

    def set_slot_count(self, slot_count):
        self.slot_count = slot_count
        self.slot_img = make_final_image(create_tiled_image(self.image_path, self.width, self.height * self.slot_count))
        self.canvas.itemconfig(self.image_id, image=self.slot_img)

    def get_data(self):
        data = super().get_data()
        del data["image_path"]
        del data["width"]
        del data["height"]
        data["slot_count"] = self.slot_count
        return data

    def get_slot_coords(self):
        data = {}
        for i in range(self.slot_count):
            data[f"slot_{i+1}"] = {
                "x": self.x,
                "y": self.y + self.height * i,
                "width": self.width,
                "height": self.height,
            }
        return data