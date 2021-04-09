from datetime import datetime
from Qt import QtWidgets


class DateTimeEdit(QtWidgets.QDateTimeEdit):

    def __init__(self, property_, parent=None):
        QtWidgets.QDateTimeEdit.__init__(self, parent)
        self.property_ = property_
        self.setDateTime(datetime.fromtimestamp(self.property_.value))
        self.setDisplayFormat("yyyy'-'MM'-'dd' 'hh':'mm")
        self.setCalendarPopup(True)
        self.clearMaximumDateTime()
        self.clearMinimumDateTime()
        self.dateTimeChanged.connect(self._value_changed)

    def _value_changed(self, value):
        self.property_.value = value.toTime_t()
        if not self.property_.is_valid():
            self.setStyleSheet("background-color: red")
        else:
            self.setStyleSheet("")
