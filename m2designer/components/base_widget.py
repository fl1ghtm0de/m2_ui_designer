from tkinter import Menu
from ctk_signal import Signal
from tools.image_tools import open_image

class WindowIndexManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(WindowIndexManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.used_index_list = {}

    def get_next_index(self, _type):
        if self.used_index_list.get(_type, None) is None:
            self.used_index_list[_type] = []

        if len(self.used_index_list[_type]) == 0:
            index = 0
        else:
            # Sort the list of used indices
            sorted_indices = sorted(self.used_index_list[_type])

            # Find the smallest missing index
            index = None
            for i in range(len(sorted_indices)):
                if sorted_indices[i] != i:
                    index = i
                    break

            # If no missing index is found, use the next highest index
            if index is None:
                index = sorted_indices[-1] + 1

        self.used_index_list[_type].append(index)
        return index

    def free_index(self, _type, index):
        if self.used_index_list.get(_type, None) is not None and index in self.used_index_list[_type]:
            self.used_index_list[_type].remove(index)

class BaseWidget:
    def __init__(self, canvas, *args, **kwargs):
        self.index_mgr = WindowIndexManager()
        self.x = kwargs.pop("x", 0)
        self.y = kwargs.pop("y", 0)
        self.text = kwargs.pop("text", None)
        self.__index = self.index_mgr.get_next_index(type(self))
        self.name = kwargs.pop("name", f"{str(self)}_{self.__index}")
        self.style = kwargs.pop("style", [])
        self.width = kwargs.pop("width", 100)
        self.height = kwargs.pop("height", 100)
        self.image = kwargs.pop("image", None)
        self.image_path = kwargs.pop("image_path", None)
        self.canvas = canvas
        self.parent = kwargs.pop("parent", None)
        self.resizable = kwargs.pop("resizable", False)
        self.resize_type = kwargs.pop("resize_type", None)
        self.resize_locked = False
        self.lock_vertical_resize = kwargs.pop("lock_vertical_resize", False)

        if self.parent is not None:
            self.x += self.parent.x
            self.y += self.parent.y

        self.image_id = self.canvas.create_image(self.x, self.y, image=self.image, anchor='nw')
        self.text_id = self.canvas.create_text(self.x+self.width//2, self.y+self.height//2, text=self.text, font=('Helvetica 9'), fill="white",)

        self.canvas.tag_bind(self.image_id, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.image_id, "<B1-Motion>", self.on_drag)

        self.canvas.tag_bind(self.text_id, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.text_id, "<B1-Motion>", self.on_drag)

        self.canvas.tag_bind(self.image_id, "<ButtonRelease-1>", lambda event: self.on_drop("widget", event))
        self.canvas.tag_bind(self.image_id, "<Button-2>", self.show_context_menu)
        self.canvas.tag_bind(self.image_id, "<Button-3>", self.show_context_menu)

        self.canvas.tag_bind(self.text_id, "<Button-2>", self.show_context_menu)
        self.canvas.tag_bind(self.text_id, "<Button-3>", self.show_context_menu)

        self.dragged_signal = Signal(BaseWidget, int, int)
        self.dragged_handle_signal = Signal(BaseWidget, int, float, float, float, float)
        self.resized_signal = Signal(BaseWidget, int, int)
        self.delete_signal = Signal(BaseWidget)
        self.unbind_from_parent_signal = Signal(BaseWidget)
        self.bind_to_parent_signal = Signal(BaseWidget)
        self.clicked_signal = Signal(dict)
        self.arrow_drag_signal = Signal(int, int)
        self.inc_zindex_signal = Signal(BaseWidget)
        self.dec_zindex_signal = Signal(BaseWidget)
        self.arrow_drag_signal.connect(self.on_arrow_drag)

        self.create_context_menu()
        if self.resizable:
            self.active_resize_handle = None
            self.resize_handles = self.create_resize_handles()

    def __del__(self):
        self.index_mgr.free_index(type(self), self.__index)

    def create_image(self, dir): # unused. To Do: make image resizing directly on each component class instead of using wrm
        img, width, height = open_image(dir)
        return img, width, height

    def set_text(self, text):
        if self.text is not None and text != "None":
            self.text = text
            self.canvas.itemconfigure(self.text_id, text=text)

    def get_style(self):
        return tuple(self.style)

    def get_style_string(self):
        return ", ".join(self.style)

    def create_resize_handles(self):
        size = 6
        resize_handles = []
        positions = [
            (self.x - size / 2, self.y - size / 2),
            (self.x + self.width - size / 2, self.y - size / 2),
            (self.x - size / 2, self.y + self.height - size / 2),
            (self.x + self.width - size / 2, self.y + self.height - size / 2)
        ]

        for i, pos in enumerate(positions):
            handle = self.canvas.create_rectangle(pos[0], pos[1], pos[0] + size, pos[1] + size, fill="white")
            self.canvas.tag_bind(handle, "<Button-1>", self.on_resize_click)
            self.canvas.tag_bind(handle, "<B1-Motion>", lambda e, index=i: self.on_resize_drag(e, index))
            resize_handles.append(handle)

        return resize_handles

    def on_click(self, event):
        self.offset_x = event.x - self.canvas.coords(self.image_id)[0]
        self.offset_y = event.y - self.canvas.coords(self.image_id)[1]
        self.clicked_signal.emit(self.get_data())

    def on_drag(self, event):
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        dx = new_x - self.x
        dy = new_y - self.y
        self.x, self.y = new_x, new_y
        self.dragged_signal.emit(self, int(dx), int(dy))
        self.clicked_signal.emit(self.get_data())

        if self.resizable:
            self.update_resize_handles()

    def on_arrow_drag(self, dx, dy):
        self.x += dx
        self.y += dy
        self.dragged_signal.emit(self, dx, dy)
        self.clicked_signal.emit(self.get_data())
        if self.resizable:
            self.update_resize_handles()

    def on_resize_click(self, event):
        if not self.resize_locked:
            # self.active_resize_handle = self.resize_handles[index]
            self.offset_x = event.x
            self.offset_y = event.y

    def on_resize_drag(self, event, index):
        if not self.resize_locked:
            # index = self.resize_handles.index(self.active_resize_handle)
            dx = event.x - self.offset_x
            dy = event.y - self.offset_y
            if self.lock_vertical_resize:
                dy = 0

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

            self.clicked_signal.emit(self.get_data())

            self.offset_x = event.x
            self.offset_y = event.y

    def update_resize_handles(self):
        size = 6
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
        # success, parent = self.bind_to_parent_signal.emit(self)
        # if success:
        #     self.parent = parent
        # else:
        #     self.unbind_from_parent_signal.emit(self)
        #     self.parent = None


    def move(self, dx, dy):
        self.dragged_signal.emit(self, dx, dy)

    def get_position(self):
        bbox = self.canvas.bbox(self.image_id)
        return bbox[0], bbox[1]

    def get_size(self):
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
        self.context_menu.add_command(label="Lock Size", command=lambda: self.disable_resizing(True))
        self.context_menu.add_command(label="Unlock Size", command=lambda: self.disable_resizing(False))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete", command=self.destroy)

    def disable_resizing(self, state:bool):
        self.resize_locked = state
        for handle in self.resize_handles:
            if state:
                self.canvas.itemconfig(handle, fill="red")
            else:
                self.canvas.itemconfig(handle, fill="white")

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
        self.clicked_signal.emit(self.get_data())

    def show_context_menu(self, event):
        self.clicked_signal.emit(self.get_data())
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def get_data(self):
        data = {
            "object" : self,
            "x" : int(self.x),
            "y" : int(self.y),
            "width" : self.width,
            "height" : self.height,
            "type" : str(self),
            "name" : self.name,
            "style" : self.style,
            "image_path" : self.image_path,
        }

        if self.text is not None:
            data["text"] = self.text

        # if self.parent is not None:
        #     data["parent_type"] = str(self.parent)
        #     data["parent_name"] = self.parent.name
        #     data["parent_x"] = self.parent.x
        #     data["parent_y"] = self.parent.y
        #     data["parent_width"] = self.parent.width
        #     data["parent_height"] = self.parent.height
            # data["x_relative"] = self.x - self.parent.x
            # data["y_relative"] = self.y - self.parent.y

        return data

    def get_uiscript_data(self):
        data = self.get_data()
        del data["object"]
        if (style := data.get("style", None)) is not None and len(style) == 0:
            del data["style"]
        if self.parent is not None:
            data["x"] -= int(self.parent.x)
            data["y"] -= int(self.parent.y)
        else:
            data["x"] = 0
            data["y"] = 0
        data["children"] = []
        return data