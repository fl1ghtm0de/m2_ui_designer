from tools.utils import flattenDict, file_exists
from tools.uiscript_im_export import generate_python_file
from components.board import Board
from components.button import Button
from components.base_widget import BaseWidget
from components.thinboard import Thinboard
from components.slot import Slot
from components.text import Text
from components.image import Image
from components.titlebar import Titlebar
from tools.image_tools import create_tiled_image, add_borders, make_final_image, stretch_image, create_titlebar
from ctk_signal import Signal
from exceptions import ComponentResizingError
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
            self.clicked_signal = Signal(dict)
            self.error_message_signal = Signal(str, str)
            self.curr_widget = None
            self.obj_type_map = {
                "button" : {"obj" : Button, "resize_type" : "stretch"},
                "board" : {"obj" : Board, "resize_type" : "tile"},
                "thinboard" : {"obj" : Thinboard, "resize_type" : "stretch"},
                "slot" : {"obj" : Slot, "resize_type" : "stretch"},
                "text" : {"obj" : Text, "resize_type" : "stretch"},
                "image" : {"obj" : Image, "resize_type" : None},
                "titlebar" : {"obj" : Titlebar, "resize_type" : "tile"},
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

    def __emit_clicked(self, data):
        widget = data.pop("object")
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

        self.clicked_signal.emit(data)

    def move_handles(self, widget, handle_id, x, y, x2, y2):
        self.canvas.coords(handle_id, x, y, x2, y2)

    def apply_entry_input(self, attr, value):
        print(attr, value)
        widget = self.curr_widget
        success = False
        if widget is not None:
            if attr == "x":
                curr_x, _ = self.canvas.coords(widget.image_id)
                if not curr_x:
                    return

                dx = value - curr_x
                self.move_widget(widget, dx, 0)
                success = True

            elif attr == "y":
                _, curr_y = self.canvas.coords(widget.image_id)
                if not curr_y:
                    return

                dy = value - curr_y
                self.move_widget(widget, 0, dy)
                success = True

            elif attr == "width":
                curr_width, _ = widget.get_size()
                if curr_width != value and widget.resizable and not widget.resize_locked:
                    if widget.resize_type is not None:
                        self.recalculate_image(widget, value, widget.height)
                    widget.width = value
                    widget.update_resize_handles()
                    success = True

            elif attr == "height":
                _, curr_height = widget.get_size()
                if curr_height != value and widget.resizable and not widget.resize_locked:
                    if widget.resize_type is not None:
                        self.recalculate_image(widget, widget.width, value)
                    widget.height = value
                    widget.update_resize_handles()
                    success = True

            elif attr == "slot_count":
                widget.set_slot_count(value)
                success = True

            elif attr == "text":
                widget.set_text(value)
                success = True

            elif attr == "image_path":
                if file_exists(value):
                    widget.set_image(value)
                    success = True
                else:
                    self.error_message_signal.emit("Error", f"File at {value} not found")

            elif attr == "style":
                if value in widget.style:
                    widget.style.remove(value)
                else:
                    widget.style.append(value)

            else:
                setattr(widget, attr, value)
                success = True

        return success

    def move_widget_absolute(self, x, y, x_parent, y_parent, width, height, wdg_name, style, text, widget=None):
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

            if wdg_name != widget.name:
                widget.name = wdg_name

            if style != widget.style:
                widget.style = style

            if text != widget.text and widget.text is not None:
                widget.set_text(text)

            if (curr_width != width or curr_height != height) and widget.resizable and not widget.resize_locked:
                if widget.resize_type is not None:
                    self.recalculate_image(widget, width, height)
                widget.width = width
                widget.height = height
                widget.update_resize_handles()

    def move_widget(self, widget, dx, dy):
        if hasattr(self, "canvas"):
            self.canvas.move(widget.image_id, dx, dy)
            if widget.text is not None:
                self.canvas.move(widget.text_id, dx, dy)
            if widget.resizable:
                for handle_id in widget.resize_handles:
                    self.canvas.move(handle_id, dx, dy)

            children = flattenDict(self.get_child_widgets(widget))
            if children:
                for child in children:
                    self.canvas.move(child.image_id, dx, dy)
                    if child.text is not None:
                        self.canvas.move(child.text_id, dx, dy)
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
        if item.text is not None:
            self.canvas.tag_raise(item.text_id)
        # if item.resizable:
        #     for handle in item.resize_handles:
        #         self.canvas.tag_raise(handle)

    def dec_z_index(self, item):
        self.canvas.tag_lower(item.image_id)
        if item.text is not None:
            self.canvas.tag_lower(item.text_id)
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
        for child in children + [obj]:
            self.canvas.delete(child.image_id)
            child.__del__()
            if child.resizable:
                for handle_id in child.resize_handles:
                    self.canvas.delete(handle_id)
            if child.text is not None:
                self.canvas.delete(child.text_id)
        self.__delete_widget_internally(obj)

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
            new_img = None
            if obj.resize_type == "tile":
                try:
                    if isinstance(obj, Titlebar):
                        new_img = create_titlebar(obj.tb_left, obj.tb_center, obj.tb_right, width)
                    elif isinstance(obj, Board):
                        new_img = create_tiled_image(obj.image_path, width, height)
                        new_img = add_borders(new_img)
                        new_img = make_final_image(new_img)
                    else:
                        raise ComponentResizingError(f"tile-resizing not defined for component-type: {obj}")
                except ValueError as e:
                    print(e)
                    return

            elif obj.resize_type == "stretch":
                corner_radius = 4
                if width < corner_radius * 2 + 1:
                    width = corner_radius * 2 + 1
                if height < corner_radius * 2 + 1:
                    height = corner_radius * 2 + 1

                new_img = stretch_image(obj.image_path, width, height, corner_radius)

            if new_img is not None:
                self.til_img_map[obj.image_id] = new_img
                self.canvas.itemconfig(obj.image_id, image=self.til_img_map[obj.image_id])

    def generate_uiscript(self):
        data = {
            "name" : "MainWindow",
            "x" : 0,
            "y" : 0,
            "style" : ["movable", "float"],
            "width" : self.curr_widget.width,
            "height" : self.curr_widget.height,
            **self.parse_to_uiscript_format()
        }
        generate_python_file("testui.py", data, "uiScriptLocale", "item", "app")

    def parse_to_uiscript_format(self):
        children = {self.curr_widget : self.get_child_widgets(self.curr_widget).copy()}
        data = {"children": []}

        stack = [(children, data)]

        while stack:
            current_children, current_data = stack.pop()

            for key, value in current_children.items():
                uis_data = key.get_uiscript_data()
                current_data["children"].append(uis_data)

                if isinstance(value, dict) and len(value.keys()) > 0:
                    stack.append((value, uis_data))

        return data
            # children = flattenDict(self.get_child_widgets(self.curr_widget))
            # data = {
            #     "name" : self.curr_widget.name,
            #     "x" : 0,
            #     "y" : 0,
            #     "style" : self.curr_widget.get_style(),
            #     "width" : self.curr_widget.width,
            #     "height" : self.curr_widget.height,
            #     "children" : [
            #         {
            #             "name" : "board",
            #             "type" : "board",
            #             "style" : ("attach",),
            #             "x" : 0,
            #             "y" : 0,
            #             "width" : self.curr_widget.width,
            #             "height" : self.curr_widget.height,
            #             "children" : [
            #                 {
            #                     "name" : "TitleBar",
            #                     "type" : "titlebar",
            #                     "style" : ("attach",),
            #                     "x" : 6,
            #                     "y" : 6,
            #                     "width" : self.curr_widget.width - 15,
            #                     "color" : "yellow",
            #                 }
            #             ]
            #         }
            #     ]
            # }

            # for child in children:
            #     data["children"].append({
            #         # IMPLEMENT
            #         })


            # # parent_x, parent_y = widget.parent.x, widget.parent.y

            # generate_python_file("testui.py", data, "uiScriptLocale", "item", "app")



        # window_data = {
        #     "name": "Acce_CombineWindow",
        #     "x": 0,
        #     "y": 0,
        #     "style": (
        #         "movable",
        #         "float",
        #     ),
        #     "width": 215,
        #     "height": 270,
        #     "children": (
        #         {
        #             "name": "board",
        #             "type": "board",
        #             "style": (
        #                 "attach",
        #             ),
        #             "x": 0,
        #             "y": 0,
        #             "width": 215,
        #             "height": 270,
        #             "children": (
        #                 {
        #                     "name": "TitleBar",
        #                     "type": "titlebar",
        #                     "style": (
        #                         "attach",
        #                     ),
        #                     "x": 6,
        #                     "y": 6,
        #                     "width": 200,
        #                     "color": "yellow",
        #                     "children": (
        #                         {
        #                             "name": "TitleName",
        #                             "type": "text",
        #                             "x": 95,
        #                             "y": 3,
        #                             "text": "uiScriptLocale.ACCE_COMBINE",
        #                             "text_horizontal_align": "center",
        #                         },
        #                     ),
        #                 },
        #                 {
        #                     "name": "Acce_Combine",
        #                     "type": "image",
        #                     "x": 9,
        #                     "y": 35,
        #                     "image": "acce/acce_combine.tga",
        #                     "children": (
        #                         {
        #                             "name": "AcceSlot",
        #                             "type": "slot",
        #                             "x": 3,
        #                             "y": 3,
        #                             "width": 200,
        #                             "height": 150,
        #                             "slot": (
        #                                 {
        #                                     "index": 0,
        #                                     "x": 78,
        #                                     "y": 7,
        #                                     "width": 32,
        #                                     "height": 32,
        #                                 },
        #                                 {
        #                                     "index": 1,
        #                                     "x": 78,
        #                                     "y": 60,
        #                                     "width": 32,
        #                                     "height": 32,
        #                                 },
        #                                 {
        #                                     "index": 2,
        #                                     "x": 78,
        #                                     "y": 115,
        #                                     "width": 32,
        #                                     "height": 32,
        #                                 },
        #                             ),
        #                         },
        #                         {
        #                             "name": "Main",
        #                             "type": "text",
        #                             "text": "uiScriptLocale.ACCE_MAIN",
        #                             "text_horizontal_align": "center",
        #                             "x": 97,
        #                             "y": 43,
        #                         },
        #                         {
        #                             "name": "serve",
        #                             "type": "text",
        #                             "text": "uiScriptLocale.ACCE_SERVE",
        #                             "text_horizontal_align": "center",
        #                             "x": 97,
        #                             "y": 98,
        #                         },
        #                         {
        #                             "name": "Result",
        #                             "type": "text",
        #                             "text": "uiScriptLocale.ACCE_RESULT",
        #                             "text_horizontal_align": "center",
        #                             "x": 97,
        #                             "y": 155,
        #                         },
        #                     ),
        #                 },
        #                 {
        #                     "name": "NeedMoney",
        #                     "type": "text",
        #                     "text": "",
        #                     "text_horizontal_align": "center",
        #                     "x": 105,
        #                     "y": 215,
        #                 },
        #                 {
        #                     "name": "AcceptButton",
        #                     "type": "button",
        #                     "x": 40,
        #                     "y": 235,
        #                     "text": "uiScriptLocale.OK",
        #                     "default_image": "d:/ymir work/ui/public/middle_button_01.sub",
        #                     "over_image": "d:/ymir work/ui/public/middle_button_02.sub",
        #                     "down_image": "d:/ymir work/ui/public/middle_button_03.sub",
        #                 },
        #                 {
        #                     "name": "CancelButton",
        #                     "type": "button",
        #                     "x": 114,
        #                     "y": 235,
        #                     "text": "uiScriptLocale.CANCEL",
        #                     "default_image": "d:/ymir work/ui/public/middle_button_01.sub",
        #                     "over_image": "d:/ymir work/ui/public/middle_button_02.sub",
        #                     "down_image": "d:/ymir work/ui/public/middle_button_03.sub",
        #                 },
        #             ),
        #         },
        #     ),
        # }


        # name = kwargs.pop("name", "")
        # x = kwargs.pop("x", 0)
        # y = kwargs.pop("y", 0)
        # style = kwargs.pop("style", ("movable, float"))
        # width = kwargs.pop("width", 0)
        # height = kwargs.pop("height", 0)