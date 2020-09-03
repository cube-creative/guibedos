"""
Flow Layout

Presents in 2D a 1D list of Widgets

Adapted from https://github.com/PySide/Examples/blob/master/examples/layouts/flowlayout.py

This file is licensed under GPLv2
"""
from Qt import QtCore
from Qt import QtWidgets


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1, expand_last=(False, False)):
        QtWidgets.QLayout.__init__(self, parent)
        self.item_list = []
        self._expand_h = expand_last[0]
        self._expand_v = expand_last[1]
        self._expand_last = expand_last[0] or expand_last[1]

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.item_list.append(item)

    def count(self):
        return len(self.item_list)

    def insertWidget(self, index, widget):
        self.addWidget(widget)
        self.item_list.insert(index, self.item_list.pop(-1))

    def itemAt(self, index):
        if index >= 0 and index < len(self.item_list):
            return self.item_list[index]
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.item_list):
            return self.item_list.pop(index)

        return None

    def removeAt(self, index):
        item = self.takeAt(index)
        if item is None:
            return None

        item.widget().setParent(None)
        item.widget().deleteLater()
        return True

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.do_layout(QtCore.QRect(0, 0, width, 0))
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def do_layout(self, rect, test_only=True):
        margins = self.contentsMargins()
        start_x = rect.x() + margins.left()
        start_y = rect.y() + margins.top()

        x = start_x
        y = start_y
        line_height = 0

        for item in self.item_list:
            widget = item.widget()

            if not widget.isVisible():
                continue

            space_x = self.spacing() + widget.style().layoutSpacing(
                QtWidgets.QSizePolicy.PushButton, QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal
            )
            space_y = self.spacing() + widget.style().layoutSpacing(
                QtWidgets.QSizePolicy.PushButton, QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical
            ) + 1

            next_x = x + widget.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = start_x
                y = y + line_height + space_y
                next_x = x + widget.sizeHint().width() + space_x
                line_height = 0

            if item == self.item_list[-1] and self._expand_last:
                width = rect.width() - x - 1 if self._expand_h else item.sizeHint().width()
                height = rect.height() - y - 1 if self._expand_v else item.sizeHint().height()
                size = QtCore.QSize(width, height)
            else:
                size = item.sizeHint()

            if not test_only:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), size))

            x = next_x

            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()
