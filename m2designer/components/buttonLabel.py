from components.draggableLabel import DraggableLabel
from PIL import Image
from customtkinter import CTkImage

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

    def __init__(self, button_type, *args, **kwargs):
        button_type = button_type.lower()
        width = Button.sizeMapping.get(button_type, (0, 0))[0]
        height = Button.sizeMapping.get(button_type, (0, 0))[1]
        img_path = f"C:/Users/vital/Projects/m2_ui_designer/m2designer/images/button/{button_type}_button.png"
        img = CTkImage(Image.open(img_path), size=(width, height))
        super().__init__(image=img, width=width, height=height, *args, **kwargs)
