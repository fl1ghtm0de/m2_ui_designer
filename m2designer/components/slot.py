from components.draggableLabel import DraggableLabel
from tools.image_tools import stretch_image
from ConfigLoader import Config

class Slot(DraggableLabel):
    def __init__(self, canvas, *args, **kwargs):
        width = kwargs.pop("width", 0)
        height = kwargs.pop("height", 0)
        cfg_loader = Config()
        self.stretch_img = stretch_image(cfg_loader.slot, width, height, 3)
        super().__init__(canvas=canvas, width=width, height=height, image=self.stretch_img, image_path=cfg_loader.slot, resizable=True, *args, **kwargs)

    def __str__(self):
        return f"Slot"