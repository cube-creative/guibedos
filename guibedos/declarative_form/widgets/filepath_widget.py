import os
try:
    from Qt import QtWidgets
except ImportError:
    from qtpy import QtWidgets


class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args):
        QtWidgets.QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, False)
        self.setFileMode(self.ExistingFiles)

        self.selected_files = list()

        self.open_button = self._hack_button()
        self.tree = self.findChild(QtWidgets.QTreeView)

    def _hack_button(self):
        buttons = self.findChildren(QtWidgets.QPushButton)
        open_button = [x for x in buttons if 'open' in str(x.text()).lower()][0]
        open_button.clicked.disconnect()
        open_button.clicked.connect(self.openClicked)
        return open_button

    def openClicked(self):
        indexes = self.tree.selectionModel().selectedIndexes()
        files = []
        for index in indexes:
            if index.column() == 0:
                files.append(os.path.normpath(os.path.join(
                    str(self.directory().absolutePath()),
                    str(index.data()))
                ))
        self.selected_files = files
        self.close()


class FilepathWidget(QtWidgets.QWidget):

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
        dialog = FileDialog()
        dialog.exec_()

        selected = dialog.selectedFiles()
        if selected:
            self.text.setText(selected[0])
            self._value_changed(selected[0])
            return

        selected = dialog.selectedFiles()
        if selected:
            self.text.setText(selected[0])
            self._value_changed(selected[0])

    def _value_changed(self, value):
        self.property_.value = value
        if not self.property_.is_valid():
            self.text.setStyleSheet("background-color: red")
        else:
            self.text.setStyleSheet("")
