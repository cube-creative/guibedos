from Qt import QtWidgets


class LabelWidget(QtWidgets.QLabel):

    def __init__(self, property_, parent=None):
        QtWidgets.QLabel.__init__(self, property_.caption, parent)
        self.property_ = property_
