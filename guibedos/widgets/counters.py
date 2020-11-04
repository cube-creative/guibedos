from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QWidget, QScrollArea, QPushButton, QVBoxLayout, QLabel
from guibedos.helpers import clear_layout
from guibedos.constants import PROPERTY_SIDE_STROKED


class Counters(QScrollArea):
    button_clicked = Signal(object, object)
    SPACING = 2

    def __init__(self, parent=None):
        QScrollArea.__init__(self, parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(Counters.SPACING)

        widget = QWidget()
        widget.setLayout(self._layout)
        self.setWidget(widget)

        self.setFixedWidth(200)
        self.checked_buttons = dict()

    def set(self, counters):
        previous_buttons = self.checked_buttons.copy()
        self.clear()

        for column, counter in counters.items():
            for entry, value in counter.items():
                checked = previous_buttons.get(entry, False)
                self.checked_buttons[entry] = checked

                button = QPushButton('{} {}'.format(entry, value))
                button.setProperty(PROPERTY_SIDE_STROKED, checked)
                button.clicked.connect(self._clicked)
                self._layout.addWidget(button)

            self._layout.addWidget(QLabel())

        self._layout.addWidget(QWidget())
        self._layout.setStretch(self._layout.count() - 1, 100)

    def clear(self):
        clear_layout(self._layout)
        self.checked_buttons = dict()

    def _clicked(self):
        button = self.sender()
        checked = not button.property(PROPERTY_SIDE_STROKED)

        entry = button.text().split()[0]
        self.checked_buttons[entry] = checked

        button.setProperty(PROPERTY_SIDE_STROKED, checked)

        self.button_clicked.emit(entry, self.checked_buttons)
