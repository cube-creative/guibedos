from Qt import QtWidgets


class DirpathWidget(QtWidgets.QWidget):

    def __init__(self, property_, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.text = QtWidgets.QLineEdit()
        self.browse = QtWidgets.QPushButton('Browse ...')
        self.browse.clicked.connect(self._browse_clicked)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.text)
        layout.addWidget(self.browse)

        self.property_ = property_
        self.text.textChanged.connect(self._value_changed)
        self.text.setText(property_.value)

    def _browse_clicked(self):
        dirpath = QtWidgets.QFileDialog.getExistingDirectory(directory=self.property_.value)
        if dirpath:
            self.text.setText(dirpath)
            self._value_changed(dirpath)

    def _value_changed(self, value):
        self.property_.value = value
        if not self.property_.is_valid():
            self.text.setStyleSheet("background-color: red")
        else:
            self.text.setStyleSheet("")
