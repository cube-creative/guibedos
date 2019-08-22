from Qt import QtWidgets
from guibedos.widgets import FlowLayout
# TODO : this is not part of the widgets packages because maker cannot be imported from there -> "find a better way"
try:
    import maker
    from constants import *
except ModuleNotFoundError as e:
    from . import maker
    from .constants import *


class GroupBox(QtWidgets.QGroupBox):

    def __init__(self, property_, parent=None):
        QtWidgets.QGroupBox.__init__(self, property_.caption, parent)
        self.property_ = property_

        layout = {
            VERTICAL: QtWidgets.QVBoxLayout,
            HORIZONTAL: QtWidgets.QHBoxLayout,
            FLOW: FlowLayout
        }[self.property_.layout](self)
        layout.setContentsMargins(0, 5, 0, 0)

        subwidgets = list()
        for subdata in property_.properties:
            new_widget = maker.make_widget(subdata, self)
            subwidgets.append(new_widget)

        self.subwidgets = subwidgets
