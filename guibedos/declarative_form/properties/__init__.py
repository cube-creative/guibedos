__all__ = [
    'Text',
    'Enum',
    'Bool',
    'List',
    'Label',
    'Integer',
    'Filepath',
    'Group',
    'Datetime'
]

from .text import Text
from .enum import Enum
from .bool_ import Bool
from .datetime import Datetime
from .list_ import List
from .label import Label
from .integer import Integer
from .filepath import Filepath
from ..constants import *


class Group(object):
    def __init__(self, name, caption, properties, layout=VERTICAL):
        self.name = name
        self.caption = caption
        self.properties = properties
        self.layout = layout
