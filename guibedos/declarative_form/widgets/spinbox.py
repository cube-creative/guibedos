try:
    from Qt import QtWidgets
except ImportError:
    from qtpy import QtWidgets
_MAX = 2147483647


class SpinBox(QtWidgets.QSpinBox):

    def __init__(self, property_, parent=None):
        QtWidgets.QSpinBox.__init__(self, parent)
        self.property_ = property_

        if property_ is not None \
                and property_.range is not None \
                and property_.range[0] is not None:
            self.setMinimum(property_.range[0])
        else:
            self.setMinimum(-_MAX)

        if property_ is not None \
                and property_.range is not None \
                and property_.range[1] is not None:
            self.setMaximum(property_.range[1])
        else:
            self.setMaximum(_MAX)

        self.setValue(property_.value)

        self.valueChanged.connect(self._value_changed)

    def _value_changed(self, value):
        self.property_.value = value
