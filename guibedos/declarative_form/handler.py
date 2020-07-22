class InteractionHandler:
    def __init__(self):
        self.widgets = {}

    def _get_property(self, given_property, widgets):
        for property, widget in widgets.items():
            if property.name == given_property:
                return property

            if type(widget) == dict:
                result = self._get_property(given_property, widget)
                if result:
                    return result

        return False

    def _get_widget(self, given_property, widgets):
        for property, widget in widgets.items():
            if property.name == given_property.name:
                return widget

            if type(widget) == dict:
                result = self._get_widget(given_property, widget)
                if result:
                    return result

        return False

    def widget(self, widget):
        return self._get_widget(widget, self.widgets)

    def property(self, property_name):
        return self._get_property(property_name, self.widgets)

    def assign(self, widgets):
        self.widgets = widgets

    def register(self, property, callback):
        if type(property) == str:
            property = self.property(property)

        self.widget(property).callback(callback=callback, sender=property)
