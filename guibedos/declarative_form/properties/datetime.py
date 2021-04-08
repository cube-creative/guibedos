import datetime
from .base_property import BaseProperty


class Datetime(BaseProperty):

    @property
    def value(self):
        return self._value.isoformat()

    @value.setter
    def value(self, value):
        if isinstance(value, datetime.datetime):
            self._value = value

    def to_datetime(self):
        return self._value

    def _validate(self):
        return True
