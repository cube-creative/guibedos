class InteractionHandler:
    def __init__(self):
        self.widgets = {}

    def _widget_is_found(self, property, given_property):
        if type(given_property) == str:
            return property.name == given_property
        else:
            return property.name == given_property.name

    def _get_widget(self, given_property, widgets):
        for property, widget in widgets.items():
            if self._widget_is_found(property, given_property):
                return (widget, property)

            if type(widget) == dict:
                result = self._get_widget(given_property, widget)
                if result:
                    return result

        return False

    def assign(self, widgets):
        self.widgets = widgets

    def widget(self, property):
        return self._get_widget(property, self.widgets)[0]

    def property(self, property):
        if type(property) == str:
            return self._get_widget(property, self.widgets)[1]
        else:
            return property

    def register(self, property, callback):
        self.widget(property).callback(callback=callback, sender=self.property(property))
