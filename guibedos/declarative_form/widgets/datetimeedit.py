from datetime import datetime
from Qt import QtWidgets

class DateTimeEdit(QtWidgets.QDateTimeEdit):

    def __init__(self, property_, parent=None):
        self.property_ = property_
        QtWidgets.QDateTimeEdit.__init__(self, datetime.fromtimestamp(self.property_.value), parent)
        self.setCalendarPopup(True)
        self.dateTimeChanged.connect(self._value_changed)

    def _value_changed(self, value):
        self.property_.value = value.toTime_t()
        if not self.property_.is_valid():
            self.setStyleSheet("background-color: red")
        else:
            self.setStyleSheet("")
