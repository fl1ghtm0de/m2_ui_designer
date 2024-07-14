import customtkinter as ctk
from tkinter import Canvas, PhotoImage
from Signal import Signal
class DraggableLabel:
    def __init__(self, canvas, *args, **kwargs):
        self.x = kwargs.pop("x", 0)
        self.y = kwargs.pop("y", 0)
        self.text = kwargs.pop("text", "default")
        self.width = kwargs.pop("width", 100)
        self.height = kwargs.pop("height", 100)
        self.image = kwargs.pop("image", None)
        self.canvas = canvas
        self.parent = kwargs.pop("parent", None)
        self.resizable = kwargs.pop("resizable", False)
        # self.item_id = self.canvas.create_text(self.x, self.y, text=self.text, font=("Helvetica", 16), fill="black")
        if self.parent is not None:
            self.x += self.parent.x
            self.y += self.parent.y

        self.image_id = self.canvas.create_image(self.x, self.y, image=self.til_img, anchor='nw')
        self.canvas.tag_bind(self.image_id, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.image_id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.image_id, "<ButtonRelease-1>", lambda event: self.on_drop("widget", event))

        self.dragged_signal = Signal(object, int, int)
        self.resized_signal = Signal(object, int, int)

        if self.resizable:
            self._create_resize_handles()

    def _create_resize_handles(self):
        self.handles = {
            "nw": self.canvas.create_oval(self.x-5, self.y-5, self.x+5, self.y+5, fill="red", tags="resize"),
            "ne": self.canvas.create_oval(self.x + self.width-5, self.y-5, self.x + self.width+5, self.y+5, fill="red", tags="resize"),
            "sw": self.canvas.create_oval(self.x-5, self.y + self.height-5, self.x+5, self.y + self.height+5, fill="red", tags="resize"),
            "se": self.canvas.create_oval(self.x + self.width-5, self.y + self.height-5, self.x + self.width+5, self.y + self.height+5, fill="red", tags="resize")
        }

        for handle in self.handles.values():
            self.canvas.tag_bind(handle, "<Button-1>", self.on_click)
            self.canvas.tag_bind(handle, "<B1-Motion>", self.on_resize_drag)
            self.canvas.tag_bind(handle, "<ButtonRelease-1>", lambda event: self.on_drop("handle", event))

    def _update_resize_handles(self):
        x, y = self.canvas.coords(self.image_id)
        self.canvas.coords(self.handles["nw"], x-5, y-5, x+5, y+5)
        self.canvas.coords(self.handles["ne"], x + self.width-5, y-5, x + self.width+5, y+5)
        self.canvas.coords(self.handles["sw"], x-5, y + self.height-5, x+5, y + self.height+5)
        self.canvas.coords(self.handles["se"], x + self.width-5, y + self.height-5, x + self.width+5, y + self.height+5)

    def on_click(self, event):
        # Store the initial position when dragging starts
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y

        if self.parent is not None:
            parent_x, parent_y = self.canvas.coords(self.parent.image_id)
            x, y = self.canvas.coords(self.image_id)
            if x - parent_x <= 0:
                dx = 1
            elif x + self.width >= parent_x + self.parent.width:
                dx = -1

            if y - parent_y <= 0:
                dy = 1
            elif y + self.height >= parent_y + self.parent.height:
                dy = -1

        self.dragged_signal.emit(self, dx, dy)
        if self.resizable:
            self._update_resize_handles()

        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_resize_drag(self, event):
        handle = self.canvas.find_closest(event.x, event.y)[0]
        x, y = self.canvas.coords(self.image_id)
        new_x, new_y = x, y

        if handle == self.handles["nw"]:
            new_x = x + (event.x - self._drag_start_x)
            new_y = y + (event.y - self._drag_start_y)
            if new_x > x + self.width:
                new_x = x + self.width
            if new_y > y + self.height:
                new_y = y + self.height
            self.width -= new_x - x
            self.height -= new_y - y
            self.canvas.coords(self.image_id, new_x, new_y)
        elif handle == self.handles["ne"]:
            new_width = (event.x - x)
            new_y = y + (event.y - self._drag_start_y)
            if new_width < 0:
                new_width = 0
            if new_y > y + self.height:
                new_y = y + self.height
            self.width = new_width
            self.height -= new_y - y
            self.canvas.coords(self.image_id, x, new_y)
        elif handle == self.handles["sw"]:
            new_x = x + (event.x - self._drag_start_x)
            new_height = (event.y - y)
            if new_x > x + self.width:
                new_x = x + self.width
            if new_height < 0:
                new_height = 0
            self.width -= new_x - x
            self.height = new_height
            self.canvas.coords(self.image_id, new_x, y)
        elif handle == self.handles["se"]:
            new_width = (event.x - x)
            new_height = (event.y - y)
            if new_width < 0:
                new_width = 0
            if new_height < 0:
                new_height = 0
            self.width = new_width
            self.height = new_height

        # Ensure positive dimensions
        if self.width < 0:
            self.width *= -1
            new_x -= self.width
        if self.height < 0:
            self.height *= -1
            new_y -= self.height

        self.canvas.coords(self.image_id, new_x, new_y)
        self._update_resize_handles()

        self._drag_start_x = event.x
        self._drag_start_y = event.y


    def on_drop(self, caller, event):
        self._drag_data = None
        if caller == "handle":
            self.resized_signal.emit(self, int(self.width), int(self.height))

    def move(self, dx, dy):
        self.dragged_signal.emit(self, dx, dy)

    def get_position(self):
        bbox = self.canvas.bbox(self.image_id)
        return bbox[0], bbox[1]

    def get_canvas_object_size(self):
        bbox = self.canvas.bbox(self.image_id)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height

    def __str__(self):
        return self.text