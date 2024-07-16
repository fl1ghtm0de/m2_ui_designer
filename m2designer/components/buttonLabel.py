from components.draggableLabel import DraggableLabel
from PIL import Image, ImageTk
from ConfigLoader import Config
from tools.image_tools import stretch_image
class Button(DraggableLabel):
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
        img_path = Config().construct_path(Config().BUTTON_PATH, f"{self.button_type}_button.png")
        self.stretch_img = stretch_image(img_path, width, height, 3)
        super().__init__(canvas=canvas, image=self.stretch_img, image_path=img_path, width=width, height=height, *args, **kwargs)

    def __str__(self):
        return f"button {self.button_type}"