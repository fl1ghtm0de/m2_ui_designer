from customtkinter import CTkLabel

class DraggableLabel(CTkLabel):
    def __init__(self, *args, **kwargs):
        self.parent_width_callback = kwargs.pop("parent_width_callback", None)
        self.parent_height_callback = kwargs.pop("parent_height_callback", None)
        super().__init__(*args, **kwargs)
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

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

        # if self.parent_width_callback is not None:
        #     if new_x + self.winfo_width() >= self.parent_width_callback():
        #         new_x = self.parent_width_callback() - self.winfo_width()
            # elif new_x - self.winfo_width() < 0:
            #     new_x = 17 # avoid out-of-border placing

        # if self.parent_height_callback is not None:
        #     if new_y + self.winfo_height() >= self.parent_height_callback():
        #         new_y = self.parent_height_callback() - self.winfo_height()
            # elif new_y - self.winfo_height() < 0:
            #     new_y = 10 # avoid out-of-border placing

        # Move the label to the new position
        self.place(x=new_x, y=new_y)
