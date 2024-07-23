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
        # self.canvas.config(self.image_id, height=self.height*self.slot_count)

    # def create_context_menu(self):
    #     super().create_context_menu()
    #     # self.context_menu.insert_separator(6)
    #     self.context_menu.insert_command(8, label="Set Slot count", command=self.set_slot_image)
    #     self.context_menu.insert_separator(8)

    def get_data(self):
        data = super().get_data()
        del data["image_path"]
        del data["width"]
        del data["height"]
        data["slot_count"] = self.slot_count
        return data