import customtkinter as ctk
from tkinter import Canvas, PhotoImage
from Signal import Signal
from WidgetRelationshipManager import WidgetRelationshipManager
class DraggableLabel:
    def __init__(self, canvas, text, *args, **kwargs):
        self.x = kwargs.pop("x", 0)
        self.y = kwargs.pop("y", 0)
        self.width = kwargs.pop("width", 100)
        self.height = kwargs.pop("height", 100)
        self.image = kwargs.pop("image", None)
        self.canvas = canvas
        self.text = text
        self.parent = kwargs.pop("parent", None)
        print(self.parent)
        # self.item_id = self.canvas.create_text(self.x, self.y, text=self.text, font=("Helvetica", 16), fill="black")
        if self.parent is not None:
            self.x += self.parent.x
            self.y += self.parent.y

        self.image_id = self.canvas.create_image(self.x, self.y, image=self.til_img, anchor='nw')
        self.canvas.tag_bind(self.image_id, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.image_id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.image_id, "<ButtonRelease-1>", self.on_drop)

        # self.canvas.tag_bind(self.item_id, "<Button-1>", self.on_click)
        # self.canvas.tag_bind(self.item_id, "<B1-Motion>", self.on_drag)
        # self.canvas.tag_bind(self.item_id, "<ButtonRelease-1>", self.on_drop)
        self.dragged_signal = Signal(object, int, int)

        wrm = WidgetRelationshipManager()
        if self.parent is None:
            wrm.add_widget(self)
        else:
            wrm.add_child_widget(self.parent, self)

    def on_click(self, event):
        # Store the initial position when dragging starts
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        # Calculate the new position of the label
        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y

        # self.canvas.move(self.image_id, dx, dy)
        # print(dx, dy, self.canvas.coords(self.image_id))
        if self.parent is not None:
            parent_x, parent_y = self.canvas.coords(self.parent.image_id)
            x, y = self.canvas.coords(self.image_id)
            if x - parent_x <= 0:
                # print(parent_x, x)
                dx = 1
            elif x + self.width >= parent_x + self.parent.width:
                # print("OUT OF BOND")
                dx = -1

            if y - parent_y <= 0:
                dy = 1
            elif y + self.height >= parent_y + self.parent.height:
                dy = -1
        self.dragged_signal.emit(self, dx, dy)
        self._drag_start_x = event.x
        self._drag_start_y = event.y

        # bbox = self.canvas.bbox(self.image_id)
        # new_x = bbox[0]
        # new_y = bbox[1]

    def on_drop(self, event):
        pass

    def move(self, dx, dy):
        self.canvas.move(self.image_id, dx, dy)

    def get_position(self):
        bbox = self.canvas.bbox(self.image_id)
        return bbox[0], bbox[1]