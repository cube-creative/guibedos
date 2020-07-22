from Qt import QtWidgets


class ComboBox(QtWidgets.QComboBox):

    def __init__(self, property_, parent=None):
        QtWidgets.QComboBox.__init__(self, parent)
        self.property_ = property_
        self.interaction_callback = None
        self.addItems([item.caption for item in property_.items])

        self.setCurrentIndex(-1)
        for index, item in enumerate(self.property_.items):
            if item.current:
                self.setCurrentIndex(index)

        self.currentIndexChanged.connect(self._value_changed)

    def _value_changed(self, index):
        caption = self.currentText()
        current_item = None

        for item in self.property_.items:
            if item.caption == caption:
                current_item = item
                item.current = True
            else:
                item.current = False

        self.property_.value = current_item.data

        if self.interaction_callback:
            self.interaction_callback(caption, self.sender)

    def callback(self, callback, sender):
        self.interaction_callback = callback
        self.sender = sender
        self._value_changed(self.currentIndex())
