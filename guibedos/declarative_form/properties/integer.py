from .base_property import BaseProperty


class Integer(BaseProperty):
    def __init__(self, name, caption, range_=None, default=None, widget=None, validator=None):
        BaseProperty.__init__(self, name, caption, default, widget, validator)
        self.range = range_

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def _validate(self):
        lower_bound = self.range[0] is not None and self.value >= self.range[0]
        upper_bound = self.range[1] is not None and self.value <= self.range[1]
        return lower_bound and upper_bound
