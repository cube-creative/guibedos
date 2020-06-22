class InteractionHandler:
    def __init__(self):
        self.data = {}

    def _get_widget(self, given_property, data):
        for property, widget in data.items():
            if type(widget) == dict:
                widget_found = self._get_widget(given_property, widget)
                if widget_found:
                    return widget_found
            elif property == given_property:
                return widget

    def assign(self, data):
        self.data = data

    def widget(self, property):
        return self._get_widget(property, self.data)

    def register(self, property, callback):
        self.widget(property).callback(callback=callback, sender=property)
