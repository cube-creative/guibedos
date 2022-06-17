try:
    from Qt import QtWidgets
except ImportError:
    from qtpy import QtWidgets

class LineEdit(QtWidgets.QLineEdit):

    def __init__(self, property_, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.property_ = property_
        self.setText(property_.value)

        self.textChanged.connect(self._value_changed)

    def _value_changed(self, value):
        self.property_.value = value
        if not self.property_.is_valid():
            self.setStyleSheet("background-color: red")
        else:
            self.setStyleSheet("")
