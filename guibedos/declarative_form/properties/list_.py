from .base_property import BaseProperty


class List(BaseProperty):

    def __init__(self, name, caption, default, validator=None):
        BaseProperty.__init__(self, name, caption, default, None, validator)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def _validate(self):
        return True
