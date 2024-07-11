from components.draggableLabel import DraggableLabel

class MainWindowLabel(DraggableLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sel