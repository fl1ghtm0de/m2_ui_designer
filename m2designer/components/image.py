from components.base_widget import BaseWidget
from tools.image_tools import open_image, create_white_image
from tkinter import filedialog
from PIL import Image as PILImage

class Image(BaseWidget):
    def __init__(self, canvas, *args, **kwargs):
        img, img_width, img_height, file_path = self.pick_image()
        if img is None:
            img_width = 50
            img_height = 50
            img = create_white_image(img_width, img_height)
            file_path = None

        super().__init__(canvas=canvas, width=img_width, height=img_height, image=img, image_path=file_path, resizable=False, *args, **kwargs)
        # self.resize_type = "tile"

    def __str__(self):
        return f"image"

    def pick_image(self):
        file_path = filedialog.askopenfilename(
            title="Open image",
            filetypes=(("Image files", "*.png *.jpeg *.jpg *.tga"),)
        )
        if file_path:
            return *open_image(file_path), file_path
        else:
            return None, -1, -1, file_path

    def set_image(self, file_path=None):
        if file_path is None:
            img, img_width, img_height, file_path = self.pick_image()
        else:
            img, img_width, img_height = open_image(file_path)

        if img is not None:
            self.image = img
            self.image_path = file_path
            self.width = img_width
            self.height = img_height

            self.canvas.config(width=self.width, height=self.height)
            self.canvas.itemconfig(self.image_id, image=img)

    def create_context_menu(self):
        super().create_context_menu()
        # self.context_menu.insert_separator(6)
        self.context_menu.insert_command(8, label="Set Image", command=self.set_image)
        self.context_menu.insert_separator(8)
