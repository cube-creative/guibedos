from Qt import QtWidgets


class SpinBox(QtWidgets.QSpinBox):

    def __init__(self, property_, parent=None):
        QtWidgets.QSpinBox.__init__(self, parent)
        self.property_ = property_
        self.setMinimum(property_.range[0])
        self.setMaximum(property_.range[1])
        self.setValue(property_.value)

        self.valueChanged.connect(self._value_changed)

    def _value_changed(self, value):
        self.property_.value = value
