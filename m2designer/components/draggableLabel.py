import customtkinter as ctk
from Signal import Signal
class DraggableLabel(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        self.parent_width_callback = kwargs.pop("parent_width_callback", None)
        self.parent_height_callback = kwargs.pop("parent_height_callback", None)
        super().__init__(*args, **kwargs)
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        self.children_widgets = []

        self.dragged_signal = Signal(object, int, int)
        self.clicked_signal = Signal(int, int)
        self.dropped_signal = Signal(int, int)

    def on_click(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        # Calculate the new position of the label
        place_info = self.place_info()
        x = int(place_info["x"])
        y = int(place_info["y"])
        # Adjust the position based on the initial click position within the label
        new_x = x + event.x - self._drag_start_x
        new_y = y + event.y - self._drag_start_y

        self.dragged_signal.emit(self, new_x, new_y)
        # Move the label to the new position
        # self.place(x=new_x, y=new_y)
        # Update positions of child widgets
        # for child in self.children_widgets:
        #     child_x = int(child.place_info()["x"])
        #     child_y = int(child.place_info()["y"])
        #     child.place(x=new_x + child_x - x, y=new_y + child_y - y)

    def on_drop(self, event):
        # for widget in self.master.winfo_children():
        #     print(widget._text, self.is_within_bounds(widget, event))
        #     if isinstance(widget, DraggableLabel) and widget is not self:
        #         # Check if the widget is within the bounds of this label
        #         if self.is_within_bounds(widget, event):
        #             print("in inside")
        #             # Move the widget inside this label
        #             widget.add_child(self, event)
        # print("------------------------------")

        # root = self.resolve_root(self)
        # target = self.resolve_drop_dest(root)

        # print(target, self.master)

        # if target is self.master:
        #     print("abort")
        #     return

        # print("target:", target)
        # print("-----------------")
        # if isinstance(target, DraggableLabel):
        #     self_copy = self.copy_widget(self, target)
        #     self_copy.place(x=0, y=0)

        pass

    def resolve_drop_dest(self, root=None):
        for index, widget in enumerate(root.winfo_children()):
            if widget is not self:
            # if self.is_inside(widget):
            #     print("inside")
            #     return self.resolve_drop_dest(widget)
                widget.configure(text=f"widget no. {index}")
                print(f"widget no. {index}", self.is_inside(widget))
                if self.is_inside(widget):
                    if isinstance(widget, DraggableLabel) and widget.get_draggable_children():
                        self.resolve_drop_dest(widget)
                    else:
                        return widget
        return root

    def get_draggable_children(self):
        return [wdg for wdg in self.winfo_children() if isinstance(wdg, DraggableLabel)]

    def resolve_root(self, widget) -> ctk.CTk:
        if widget.master.master:
            return self.resolve_root(widget.master)
        else:
            return widget.master

    def is_inside(self, widget) -> bool:
        coords = widget.place_info()
        coordsSelf = self.place_info()

        x = widget.winfo_x()
        y = widget.winfo_y()
        width = widget.winfo_width()
        height = widget.winfo_height()

        xSelf = self.winfo_x()
        ySelf = self.winfo_y()
        widthSelf = self.winfo_width()
        heightSelf = self.winfo_height()

        # print("coordsTarget: ", f"x: {x} y: {y} width: {width} height: {height}")
        # print("coordsSelf: ", f"x: {xSelf} y: {ySelf} width: {widthSelf} height: {heightSelf}")

        # print("target: ", x, y, width, height, widget._text)
        # print("self: ", xSelf, ySelf, widthSelf, heightSelf, self._text)

        if xSelf >= x and (xSelf + widthSelf) < (x + width): # x check
            if ySelf >= y and (ySelf + heightSelf) < (x + height): # y check
                return True

        return False


    def is_within_bounds(self, widget):
        # Get the position and size of this label
        place_info = self.place_info()
        x = int(place_info["x"])
        y = int(place_info["y"])
        width = self.winfo_width()
        height = self.winfo_height()

        # Get the position of the widget
        widget_place_info = widget.place_info()
        widget_x = int(widget_place_info["x"])
        widget_y = int(widget_place_info["y"])

        # Check if the widget is within the bounds of this label
        return (x <= widget_x <= x + width and y <= widget_y <= y + height)

    def add_child(self, widget, event):
        # Calculate the new position relative to this label
        place_info = self.place_info()
        parent_x = int(place_info["x"])
        parent_y = int(place_info["y"])
        widget_x = int(widget.place_info()["x"])
        widget_y = int(widget.place_info()["y"])
        new_x = widget_x - parent_x
        new_y = widget_y - parent_y

        # Move the widget to the new position
        widget.place(x=new_x, y=new_y, in_=self)

        # Add the widget to the list of children
        self.children_widgets.append(widget)

    def copy_widget(self, original_widget, parent):
        # Get the class of the original widget
        widget_class = original_widget.__class__

        # Create a new widget with the same class
        new_widget = widget_class(master=parent, button_type="large")

        # Copy configuration from the original widget to the new widget
        for key in original_widget.keys():
            try:
                new_widget.configure({key: original_widget.cget(key)})
            except:
                pass  # Some options might not be configurable this way

        return new_widget