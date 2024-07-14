from tools.utils import flattenDict
from components.mainWindow import MainWindowLabel
from components.buttonLabel import Button
from tools.tileImage import create_tiled_image, add_borders, make_final_image
from ConfigLoader import Config
class WidgetRelationshipManager(object):
    """singleton class to keep track of all placed widgets and their relationships
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WidgetRelationshipManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.widgets = {}
            self.til_img_list = []

    def set_canvas(self, canvas):
        self.canvas = canvas

    def move_widget(self, widget, x, y):
        if hasattr(self, "canvas"):
            self.canvas.move(widget.image_id, x, y)
            children = flattenDict(self.get_child_widgets(widget))
            if children:
                for child in children:
                    self.canvas.move(child.image_id, x, y)
                    if child.resizable:
                        for handle_id in child.handles.values():
                            self.canvas.move(handle_id, x, y)
        else:
            raise Exception("Canvas of wrm not set")

    def add_widget(self, widget_name):
        if not widget_name in self.widgets.keys():
            self.widgets[widget_name] = {}
        else:
            raise Exception("Widget with this name already exists!")

    def add_child_widget(self, parent_widget, *widgets, _widgets=None):
        if _widgets is None:
            _widgets = self.widgets

        res = _widgets.get(parent_widget, None)

        if res is None:
            for key, value in _widgets.items():
                if len(value.keys()) > 0:
                    return self.add_child_widget(parent_widget, *widgets, _widgets=value)
        else:
            for wdg in widgets:
                res[wdg] = {}

    def get_widget(self, widget_name):
        return self.widgets.get(widget_name, None)

    def get_child_widgets(self, parent_widget, widgets=None) -> dict:
        if widgets is None:
            widgets = self.widgets

        for key, value in widgets.items():
            if key is parent_widget:
                return value
            elif isinstance(value, dict):
                return self.get_child_widgets(parent_widget, value)

        return {}

    def get_parent_widgets(self, widget, widget_dict=None):
        if widget_dict is None:
            widget_dict = self.widgets

        for parent, children in widget_dict.items():
            if widget in children.keys():
                return parent
            else:
                if len(children.keys()) > 0:
                    return self.get_parent_widgets(widget, children)

        return None


    def create_window(self, x=30, y=30, width=100, height=100, text="", parent=None) -> MainWindowLabel:
        if hasattr(self, "canvas"):
            wdg = MainWindowLabel(text=text, parent=parent, canvas=self.canvas, x=x, y=y, width=width, height=height)
            wdg.dragged_signal.connect(self.move_widget)
            wdg.resized_signal.connect(self.recalculate_tiled_image)
            wdg.delete_signal.connect(self.delete_widget)
            if parent is None:
                self.add_widget(wdg)
            else:
                self.add_child_widget(parent, wdg)
            return wdg
        else:
            raise Exception("Canvas of wrm not set")

    def create_button(self, x=30, y=30, text="", parent=None) -> Button:
        if hasattr(self, "canvas"):
            wdg = Button(parent=parent, canvas=self.canvas, x=x, y=y, text=text, button_type="large")
            wdg.dragged_signal.connect(self.move_widget)
            wdg.resized_signal.connect(self.recalculate_tiled_image)
            wdg.delete_signal.connect(self.delete_widget)
            if parent is None:
                self.add_widget(wdg)
            else:
                self.add_child_widget(parent, wdg)
            return wdg
        else:
            raise Exception("Canvas of wrm not set")

    def delete_widget(self, obj):
        children = flattenDict(self.get_child_widgets(obj))
        for child in children + [obj]:
            self.canvas.delete(child.image_id)
            if child.resizable:
                for handle_id in child.handles.values():
                    self.canvas.delete(handle_id)


    def recalculate_tiled_image(self, obj, width, height):
        if isinstance(obj, MainWindowLabel):
            cfg_loader = Config()
            til_img = create_tiled_image(cfg_loader.board_base, width, height)
            til_img = add_borders(
                                    til_img,
                                    border_images={
                                        "top" : cfg_loader.top,
                                        "left": cfg_loader.left,
                                        "bottom": cfg_loader.bottom,
                                        "right": cfg_loader.right,
                                        "top_left_corner": cfg_loader.top_left_corner,
                                        "bottom_left_corner": cfg_loader.bottom_left_corner,
                                        "bottom_right_corner": cfg_loader.bottom_right_corner,
                                        "top_right_corner": cfg_loader.top_right_corner,
                                        "close_button": cfg_loader.close_button,
                                        "minimize_button": cfg_loader.minimize_button
                                },
                                )

            self.til_img_list.append(make_final_image(til_img))
            self.canvas.itemconfig(obj.image_id, image=self.til_img_list[-1])