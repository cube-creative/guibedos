from .base_property import BaseProperty


class Text(BaseProperty):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def _validate(self):
        return True
