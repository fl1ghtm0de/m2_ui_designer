from customtkinter import CTkLabel

class DraggableLabel(CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

    def on_click(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        x = self.winfo_x() - self._drag_start_x / 2 + event.x
        y = self.winfo_y() - self._drag_start_y / 2 + event.y
        self.place(x=x, y=y)
