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

    def add_widget(self, widget_name):
        if not widget_name in self.widgets.keys():
            self.widgets[widget_name] = {}
        else:
            raise Exception("Widget with this name already exists!")

    def add_child_widget(self, *parent_widgets, widget):
        parent_widget = None
        for parent in parent_widgets:
            if parent_widget is None:
                parent_widget = self.widgets.get(parent, None)
            else:
                parent_widget = parent_widget.get(parent, None)

        parent_widget[widget] = {}

    def get_widget(self, widget_name):
        return self.widgets.get(widget_name, None)

    def get_child_widgets(self, *parent_widgets):
        parent_widget = None
        for parent in parent_widgets:
            if parent_widget is None:
                parent_widget = self.widgets.get(parent, None)
            else:
                parent_widget = parent_widget.get(parent, None)

        return parent_widget
