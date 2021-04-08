from Qt import QtWidgets


class DateTimeEdit(QtWidgets.QDateTimeEdit):

    def __init__(self, property_, parent=None):
        QtWidgets.QDateTimeEdit.__init__(self, property_.to_datetime(), parent)
        self.property_ = property_
        self.setCalendarPopup(True)
        self.dateTimeChanged.connect(self._value_changed)

    def _value_changed(self, value):
        self.property_.value = value.toPython()
        if not self.property_.is_valid():
            self.setStyleSheet("background-color: red")
        else:
            self.setStyleSheet("")
