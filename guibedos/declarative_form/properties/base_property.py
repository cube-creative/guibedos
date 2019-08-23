

class BaseProperty(object):

    def __init__(self, name, caption, default=None, widget=None, validator=None):
        self.name = name
        self.caption = caption
        self.value = default
        self.widget = widget
        self.validator = validator

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, value):
        raise NotImplementedError

    def is_valid(self):
        if not self._validate():
            return False

        if self.validator:
            return self.validator(self.value)

        return True

    def _validate(self):
        raise NotImplementedError
