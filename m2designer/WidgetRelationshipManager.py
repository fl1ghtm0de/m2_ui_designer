from tools.utils import flattenDict
from components.board import Board
from components.button import Button
from components.base_widget import BaseWidget
from components.thinboard import Thinboard
from components.slot import Slot
from tools.image_tools import create_tiled_image, add_borders, make_final_image, stretch_image
from ConfigLoader import Config
from Signal import Signal
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
            self.til_img_map = {}
            self.clicked_signal = Signal(int, int, int, int, int, int, str, str)
            self.curr_widget = None
            self.obj_type_map = {
                "button" : {"obj" : Button, "resize_type" : "stretch"},
                "board" : {"obj" : Board, "resize_type" : "tile"},
                "thinboard" : {"obj" : Thinboard, "resize_type" : "stretch"},
                "slot" : {"obj" : Slot, "resize_type" : "stretch"}
            }

    def __check_overlap(self, child_wdg: BaseWidget, _dict=None) -> BaseWidget | None:
        """Checks if child_wdg is completely inside another widget. If so, it returns this widget, otherwise None."""
        if _dict is None:
            _dict = self.widgets

        bbox_child = self.canvas.bbox(child_wdg.image_id)
        highest_z_index_widget = None

        for widget_id in self.canvas.find_all():
            wdg = None
            for w in _dict.keys():
                if w.image_id == widget_id:
                    wdg = w
                    break

            if wdg is None or wdg is child_wdg:
                continue

            bbox_parent = self.canvas.bbox(wdg.image_id)
            if bbox_parent and bbox_child:
                # Check if child_wdg is completely inside wdg
                fully_inside = (bbox_parent[0] <= bbox_child[0] and
                                bbox_parent[1] <= bbox_child[1] and
                                bbox_parent[2] >= bbox_child[2] and
                                bbox_parent[3] >= bbox_child[3])
                if fully_inside:
                    highest_z_index_widget = wdg

            # Check nested children
            if isinstance(_dict[wdg], dict) and len(_dict[wdg].keys()) > 0:
                nested_widget = self.__check_overlap(child_wdg, _dict[wdg])
                if nested_widget:
                    highest_z_index_widget = nested_widget

        return highest_z_index_widget

    def set_canvas(self, canvas):
        self.canvas = canvas

    def get_curr_widget(self) -> BaseWidget:
        return self.curr_widget

    def hide_handles(self, wdg:BaseWidget):
        if wdg is not None and wdg.resizable:
            for handle in wdg.resize_handles:
                self.canvas.itemconfigure(handle, state="hidden")

    def show_handles(self, wdg:BaseWidget):
        if wdg is not None and wdg.resizable:
            for handle in wdg.resize_handles:
                self.canvas.itemconfigure(handle, state="normal")
                self.canvas.tag_raise(handle)

    def set_curr_widget(self, wdg):
        if isinstance(wdg, BaseWidget) or wdg is None:
            if wdg is None:
                self.hide_handles(self.curr_widget)
            self.curr_widget = wdg

    def __emit_clicked(self, widget):
        self.hide_handles(self.curr_widget)
        self.set_curr_widget(widget)
        self.show_handles(self.curr_widget)

        parent_x = 0
        parent_y = 0

        if widget.parent is not None:

            # parent_x, parent_y = self.canvas.coords(widget.parent.image_id)
            # x, y = self.canvas.coords(widget.image_id)
            parent_x = widget.x - widget.parent.x
            parent_y = widget.y - widget.parent.y

        self.clicked_signal.emit(int(widget.x), int(widget.y), int(parent_x), int(parent_y), int(widget.width), int(widget.height), str(widget), str(widget.parent))

    def move_handles(self, widget, handle_id, x, y, x2, y2):
        self.canvas.coords(handle_id, x, y, x2, y2)

    def move_widget_absolute(self, x, y, x_parent, y_parent, width, height, widget=None):
        if hasattr(self, "canvas"):
            if widget is None:
                widget = self.curr_widget
            if widget is None:  # case for self.curr_widget being None
                return

            curr_width, curr_height = widget.get_size()

            if widget.parent is not None:
                # If the widget has a parent, calculate the target position based on the parent
                parent_x, parent_y = widget.parent.x, widget.parent.y
                target_x = parent_x + x_parent
                target_y = parent_y + y_parent
            else:
                # If the widget doesn't have a parent, use the absolute coordinates
                target_x = x
                target_y = y

            curr_coords = self.canvas.coords(widget.image_id)
            if not curr_coords:
                return

            curr_x, curr_y = curr_coords[0], curr_coords[1]

            dx = target_x - curr_x
            dy = target_y - curr_y

            widget.x = target_x
            widget.y = target_y

            self.move_widget(widget, dx, dy)

            if (curr_width != width or curr_height != height) and not widget.resize_locked:
                self.recalculate_image(widget, width, height)
                widget.width = width
                widget.height = height
                widget.update_resize_handles()



    def move_widget(self, widget, dx, dy):
        if hasattr(self, "canvas"):
            self.canvas.move(widget.image_id, dx, dy)
            if widget.resizable:
                for handle_id in widget.resize_handles:
                    self.canvas.move(handle_id, dx, dy)

            children = flattenDict(self.get_child_widgets(widget))
            # print(self.widgets)
            # print(self.get_child_widgets(widget))
            if children:
                for child in children:
                    self.canvas.move(child.image_id, dx, dy)
                    if child.resizable:
                        for handle_id in child.resize_handles:
                            self.canvas.move(handle_id, dx, dy)
                    # Update child positions
                    child.x += dx
                    child.y += dy
            return True
        else:
            raise Exception("Canvas of wrm not set")

    def add_widget(self, widget_name):
        if not widget_name in self.widgets.keys():
            self.widgets[widget_name] = {}
        else:
            raise Exception("Widget with this name already exists!")

    def get_widget(self, widget_name):
        return self.widgets.get(widget_name, None)

    def get_child_widgets(self, parent_widget, widgets=None) -> dict:
        if widgets is None:
            widgets = self.widgets

        for key, value in widgets.items():
            if key is parent_widget:
                return value
            elif isinstance(value, dict):
                result = self.get_child_widgets(parent_widget, value)
                if result:
                    return result

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

    def remove_widget(self, widget, _dict=None) -> None | dict:
        if _dict is None:
            _dict = self.widgets

        for key, value in list(_dict.items()):
            if key == widget:
                # Found the widget, remove it and return its data
                return _dict.pop(key)
            elif isinstance(value, dict):
                # Recursively search in the nested dictionary
                result = self.remove_widget(widget, value)
                if result is not None:
                    # If the widget was found and removed in the nested dict, return the result
                    return result
        return None

    def inc_z_index(self, item):
        self.canvas.tag_raise(item.image_id)
        # if item.resizable:
        #     for handle in item.resize_handles:
        #         self.canvas.tag_raise(handle)

    def dec_z_index(self, item):
        self.canvas.tag_lower(item.image_id)
        # if item.resizable:
        #     for handle in item.resize_handles:
        #         self.canvas.tag_lower(handle)

    def remove_child_widget(self, widget, parent):
        childs = self.remove_widget(widget)
        self.widgets[widget] = childs

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

    def bind_widget_to_parent(self, widget) -> bool:
        parent = self.__check_overlap(widget)
        if parent is not None:
            self.remove_widget(widget)
            self.add_child_widget(parent, widget)
            return True, parent
        return False, None

    def create_widget(self, _type:str, **kwargs) -> BaseWidget:
        obj = self.obj_type_map.get(_type, None)
        if obj is None:
            raise Exception(f"Widget of type {_type} not existing in wrm.obj_type_map")

        if hasattr(self, "canvas"):
            parent = kwargs.get("parent", None)
            wdg = obj["obj"](**kwargs, resize_type=obj["resize_type"])
            wdg.dragged_signal.connect(self.move_widget)
            wdg.resized_signal.connect(self.recalculate_image)
            wdg.delete_signal.connect(self.delete_widget)
            wdg.dragged_handle_signal.connect(self.move_handles)
            wdg.clicked_signal.connect(self.__emit_clicked)
            wdg.unbind_from_parent_signal.connect(lambda widget: self.remove_child_widget(widget, widget.parent))
            wdg.bind_to_parent_signal.connect(self.bind_widget_to_parent)
            wdg.inc_zindex_signal.connect(self.inc_z_index)
            wdg.dec_zindex_signal.connect(self.dec_z_index)
            self.hide_handles(wdg)

            if parent is None:
                self.add_widget(wdg)
            else:
                self.add_child_widget(parent, wdg)

            print(len(self.widgets.keys()))
            return wdg
        else:
            raise Exception("Canvas of wrm not set")

    def delete_widget(self, obj):
        children = flattenDict(self.get_child_widgets(obj))
        print(obj, self.widgets)
        for child in children + [obj]:
            self.canvas.delete(child.image_id)
            if child.resizable:
                for handle_id in child.resize_handles:
                    self.canvas.delete(handle_id)
        self.__delete_widget_internally(obj)
        print(self.widgets)

    def __delete_widget_internally(self, obj, _dict=None):
        if _dict is None:
            _dict = self.widgets

        if obj in _dict:
            del _dict[obj]
            return True
        else:
            for key, value in _dict.items():
                if isinstance(value, dict):
                    if self.__delete_widget_internally(obj, value):
                        # If deletion was successful, clean up empty dictionaries
                        if not value:
                            _dict[key] = {}
                        return True
        return False


    def recalculate_image(self, obj, width, height):
        if isinstance(obj, BaseWidget):
            if obj.resize_type == "tile":
                til_img = create_tiled_image(obj.image_path, width, height)
                til_img = add_borders(til_img, obj.image_borders)
                self.til_img_map[obj.image_id] = make_final_image(til_img)
                self.canvas.itemconfig(obj.image_id, image=self.til_img_map[obj.image_id])

            elif obj.resize_type == "stretch":
                corner_radius = 4
                if width < corner_radius * 2 + 1:
                    width = corner_radius * 2 + 1
                if height < corner_radius * 2 + 1:
                    height = corner_radius * 2 + 1

                self.til_img_map[obj.image_id] = stretch_image(obj.image_path, width, height, corner_radius)
                self.canvas.itemconfig(obj.image_id, image=self.til_img_map[obj.image_id])