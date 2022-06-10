try:
    from Qt import QtWidgets
except ImportError:
    from qtpy import QtWidgets


class CheckBox(QtWidgets.QCheckBox):

    def __init__(self, property_, parent=None):
        QtWidgets.QCheckBox.__init__(self, property_.caption, parent)
        self.interaction_callback = None
        self.property_ = property_
        self.setChecked(property_.value)

        self.stateChanged.connect(self._value_changed)

    def _value_changed(self, value):
        self.property_.value = value
        if not self.property_.is_valid():
            self.setStyleSheet("background-color: red")
        else:
            self.setStyleSheet("")
            if self.interaction_callback:
                self.interaction_callback(value, self.sender)

    def callback(self, callback, sender):
        self.interaction_callback = callback
        self.sender = sender
        self._value_changed(self.isChecked())
