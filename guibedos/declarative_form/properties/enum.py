from .base_property import BaseProperty


class Enum(BaseProperty):

    class Item(object):
        def __init__(self, caption, data, current=False):
            self.caption = caption
            self.current = current
            self.data = data

    def __init__(self, name, caption, items, widget=None, validator=None):
        BaseProperty.__init__(self, name, caption, None, widget, validator)
        self.items = items

        current_item = self.items[0]
        for item in self.items:
            if item.current:
                current_item = item
                break

        for item in self.items:
            item.current = item == current_item

        self.value = current_item.data

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def _validate(self):
        return True
