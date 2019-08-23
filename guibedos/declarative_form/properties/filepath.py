import os.path
from .base_property import BaseProperty


class Filepath(BaseProperty):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def _validate(self):
        return True
        # TODO : is this relevant ?
        # if self.value is None:
        #     return False
        # return os.path.exists(self.value)
