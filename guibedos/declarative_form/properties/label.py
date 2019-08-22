from .base_property import BaseProperty


class Label(BaseProperty):
    def __init__(self, name, caption, default=None, widget=None, validator=None):
        BaseProperty.__init__(self, name, caption, default, widget, validator)

    @property
    def value(self):
        return None

    @value.setter
    def value(self, value):
        pass

    def _validate(self):
        return True
