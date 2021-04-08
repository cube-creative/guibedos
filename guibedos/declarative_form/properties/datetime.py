import datetime
from .base_property import BaseProperty


class Datetime(BaseProperty):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def _validate(self):
        if isinstance(self._value, str) or self._value is None:
            return True
        else:
            return False
