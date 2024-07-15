from tkinter import Menu
from Signal import Signal
from customtkinter import CTkOptionMenu
class DraggableLabel:
    def __init__(self, canvas, *args, **kwargs):
        self.x = kwargs.pop("x", 0)
        self.y = kwargs.pop("y", 0)
        self.text = kwargs.pop("text", "default")
        self.width = kwargs.pop("width", 100)
        self.height = kwargs.pop("height", 100)
        self.image = kwargs.pop("image", None)
        self.image_path = kwargs.pop("image_path", None)
        self.image_borders = kwargs.pop("image_borders", None)
        self.canvas = canvas
        self.parent = kwargs.pop("parent", None)
        self.resizable = kwargs.pop("resizable", False)
        self.resize_type = kwargs.pop("resize_type", "stretch")
        # self.item_id = self.canvas.create_text(self.x, self.y, text=self.text, font=("Helvetica", 16), fill="black")
        if self.parent is not None:
            self.x += self.parent.x
            self.y += self.parent.y

        self.image_id = self.canvas.create_image(self.x, self.y, image=self.image, anchor='nw')
        self.canvas.tag_bind(self.image_id, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.image_id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.image_id, "<ButtonRelease-1>", lambda event: self.on_drop("widget", event))
        self.canvas.tag_bind(self.image_id, "<Button-2>", self.show_context_menu)
        self.canvas.tag_bind(self.image_id, "<Button-3>", self.show_context_menu)
        self.dragged_signal = Signal(DraggableLabel, int, int)
        self.dragged_handle_signal = Signal(DraggableLabel, int, float, float, float, float)
        self.resized_signal = Signal(DraggableLabel, int, int)
        self.delete_signal = Signal(DraggableLabel)
        self.unbind_from_parent_signal = Signal(DraggableLabel)
        self.bind_to_parent_signal = Signal(DraggableLabel)
        self.clicked_signal = Signal(object)
        self.arrow_drag_signal = Signal(int, int)
        self.inc_zindex_signal = Signal(DraggableLabel)
        self.dec_zindex_signal = Signal(DraggableLabel)

        self.arrow_drag_signal.connect(self.on_arrow_drag)
        self.create_context_menu()
        if self.resizable:
            self.active_resize_handle = None
            self.resize_handles = self.create_resize_handles()

    def create_resize_handles(self):
        size = 8
        resize_handles = []
        positions = [
            (self.x - size / 2, self.y - size / 2),
            (self.x + self.width - size / 2, self.y - size / 2),
            (self.x - size / 2, self.y + self.height - size / 2),
            (self.x + self.width - size / 2, self.y + self.height - size / 2)
        ]

        for pos in positions:
            handle = self.canvas.create_rectangle(pos[0], pos[1], pos[0] + size, pos[1] + size, fill="red")
            self.canvas.tag_bind(handle, "<Button-1>", self.on_resize_click)
            self.canvas.tag_bind(handle, "<B1-Motion>", self.on_resize_drag)
            resize_handles.append(handle)

        return resize_handles

    def on_click(self, event):
        self.offset_x = event.x - self.canvas.coords(self.image_id)[0]
        self.offset_y = event.y - self.canvas.coords(self.image_id)[1]
        self.clicked_signal.emit(self)

    def on_drag(self, event):
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        dx = new_x - self.x
        dy = new_y - self.y
        self.x, self.y = new_x, new_y
        self.dragged_signal.emit(self, int(dx), int(dy))

        if self.resizable:
            self.update_resize_handles()

    def on_arrow_drag(self, dx, dy):
        self.x += dx
        self.y += dy
        self.dragged_signal.emit(self, dx, dy)

        if self.resizable:
            self.update_resize_handles()

    def on_resize_click(self, event):
        self.active_resize_handle = self.canvas.find_closest(event.x, event.y)[0]
        self.offset_x = event.x
        self.offset_y = event.y

    def on_resize_drag(self, event):
        if self.active_resize_handle is not None:
            index = self.resize_handles.index(self.active_resize_handle)
            dx = event.x - self.offset_x
            dy = event.y - self.offset_y

            if index == 0:  # Top-left handle
                new_x = self.x + dx
                new_y = self.y + dy
                new_width = self.width - dx
                new_height = self.height - dy
            elif index == 1:  # Top-right handle
                new_x = self.x
                new_y = self.y + dy
                new_width = self.width + dx
                new_height = self.height - dy
            elif index == 2:  # Bottom-left handle
                new_x = self.x + dx
                new_y = self.y
                new_width = self.width - dx
                new_height = self.height + dy
            elif index == 3:  # Bottom-right handle
                new_x = self.x
                new_y = self.y
                new_width = self.width + dx
                new_height = self.height + dy

            if new_width > 0 and new_height > 0:
                self.x, self.y = new_x, new_y
                self.width, self.height = new_width, new_height
                self.canvas.coords(self.image_id, self.x, self.y)
                self.resized_signal.emit(self, self.width, self.height)
                # self.canvas.itemconfig(self.image_id, image=self.resize_image(self.image, self.width, self.height))
                if self.resizable:
                    self.update_resize_handles()

            self.offset_x = event.x
            self.offset_y = event.y

    def update_resize_handles(self):
        size = 8
        positions = [
            (self.x - size / 2, self.y - size / 2),
            (self.x + self.width - size / 2, self.y - size / 2),
            (self.x - size / 2, self.y + self.height - size / 2),
            (self.x + self.width - size / 2, self.y + self.height - size / 2)
        ]

        for i, handle in enumerate(self.resize_handles):
            self.dragged_handle_signal.emit(self, handle, positions[i][0], positions[i][1], positions[i][0] + size, positions[i][1] + size)

    def on_drop(self, caller, event):
        self._drag_data = None
        # if caller == "handle":
        #     self.resized_signal.emit(self, int(self.width), int(self.height))

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

    def create_context_menu(self):
        self.context_menu = Menu(self.canvas, tearoff=0)
        self.context_menu.add_command(label="Unbind from parent", command=self.unbind_from_parent)
        self.context_menu.add_command(label="Bind to parent", command=self.bind_to_parent)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Increase z-index", command=lambda: self.inc_zindex_signal.emit(self))
        self.context_menu.add_command(label="Decrease z-index", command=lambda: self.dec_zindex_signal.emit(self))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete", command=self.destroy)

    def destroy(self):
        self.delete_signal.emit(self)

    def unbind_from_parent(self):
        self.unbind_from_parent_signal.emit(self)
        self.parent = None

    def bind_to_parent(self):
        # self.parent = None
        success, parent = self.bind_to_parent_signal.emit(self)
        if success:
            self.parent = parent

    def show_context_menu(self, event):
        self.clicked_signal.emit(self)
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()