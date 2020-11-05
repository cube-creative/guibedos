from Qt.QtCore import Signal
from Qt.QtWidgets import QWidget, QGridLayout, QTableWidget, QPushButton, QTableWidgetItem
from .color import Color


class Variables(QWidget):
    changed = Signal(object)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setMinimumWidth(500)

        self.table = QTableWidget()
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemChanged.connect(self._item_changed)
        self.table.currentItemChanged.connect(self._current_item_changed)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.setColumnCount(3)
        self.table.horizontalHeader().resizeSection(0, 200)
        self.table.horizontalHeader().resizeSection(1, 200)
        self.table.horizontalHeader().resizeSection(2, 20)

        self.new = QPushButton('New variable')
        self.new.clicked.connect(self._new)

        self.color = Color()
        self.color.changed.connect(self._color_changed)

        layout = QGridLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.color)
        layout.addWidget(self.new)

    @property
    def variables(self):
        variables = dict()

        for row_index in range(self.table.rowCount()):
            name = self.table.item(row_index, 0).text()
            value = self.table.item(row_index, 1).text()

            if value.startswith('[') and value.endswith(']'):
                value = eval(value)  # OULA LA

            variables[name] = value

        return variables

    @variables.setter
    def variables(self, variables):
        self.table.blockSignals(True)
        self.table.clear()
        for name, value in variables.items():
            self._add_row(name, value)

        self.table.blockSignals(False)
        self.changed.emit(variables)

    def _item_changed(self, item):
        self.changed.emit(self.variables)
        self._current_item_changed(item)

    def _current_item_changed(self, item):
        self.color.setEnabled(False)

        if item is None or item.column() != 1:
            return

        text = item.text().strip()
        if not (text.startswith('[') and text.endswith(']')):
            return

        r, g, b = [int(channel.strip()) for channel in text[1:-1].split(',')]

        self.color.blockSignals(True)
        self.color.set_rgb(r, g, b)
        self.color.setEnabled(True)
        self.color.blockSignals(False)

    def _color_changed(self, r, g, b):
        self.table.blockSignals(True)
        self.table.currentItem().setText(f'[{r}, {g}, {b}]')
        self.table.blockSignals(False)
        self.changed.emit(self.variables)

    def _add_row(self, name, value):
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)

        name = QTableWidgetItem(name)
        value = QTableWidgetItem(str(value))

        delete = QPushButton("X")
        delete.name_item = name
        delete.clicked.connect(self._delete)

        self.table.blockSignals(True)
        self.table.setItem(row, 0, name)
        self.table.setItem(row, 1, value)
        self.table.setCellWidget(row, 2, delete)
        self.table.blockSignals(False)

    def _new(self):
        self._add_row('new_variable', '[255, 255, 255]')
        self.changed.emit(self.variables)

    def _delete(self):
        name_item = self.sender().name_item
        self.table.removeRow(name_item.row())

        self.changed.emit(self.variables)
