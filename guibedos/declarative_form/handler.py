class InteractionHandler:
    def __init__(self):
        self.data = {}

    def get_widgets(self, name, data, widgets_found):
        for property_name, widget in data.items():
            if type(widget) == dict:
                widgets_found = self.get_widgets(name, widget, widgets_found)
            if property_name == name:
                widgets_found.append(widget)
        return widgets_found

    def assign(self, data):
        self.data = data

    def register(self, property, callback):
        for widget in self.get_widgets(property, self.data, list()):
            widget.callback(callback=callback, sender=property)
