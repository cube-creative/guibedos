class InteractionHandler:
    def __init__(self):
        self.data = {}

    def _widget_is_found(self, property, given_property):
        if type(given_property) == str:
            return property.name == given_property
        else:
            return property.name == given_property.name

    def _get_widget(self, given_property, widgets):
        for property, widget in widgets.items():
            if type(widget) == dict:
                widget_found = self._get_widget(given_property, widget)
                if widget_found:
                    return widget_found
            elif self._widget_is_found(property, given_property):
                return (widget, property)

    def assign(self, data):
        self.data = data

    def widget(self, property):
        return self._get_widget(property, self.data)[0]

    def property(self, property):
        if type(property) == str:
            return self._get_widget(property, self.data)[1]
        else:
            return property

    def register(self, property, callback):
        self.widget(property).callback(callback=callback, sender=self.property(property))
