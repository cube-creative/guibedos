from Qt.QtCore import Qt, Signal
from Qt.QtWidgets import QWidget, QScrollArea, QPushButton, QVBoxLayout, QLabel
from guibedos.helpers import clear_layout



class Counters(QScrollArea):
    button_clicked = Signal(object, object)
    SPACING = 1

    def __init__(self, parent=None):
        QScrollArea.__init__(self, parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(Counters.SPACING)

        widget = QWidget()
        widget.setLayout(self._layout)
        self.setWidget(widget)

        self.setFixedWidth(200)

    def set(self, counters):
        self.clear()

        for column, counter in counters.items():
            for entry, value in counter.items():
                button = QPushButton('{} {}'.format(entry, value))
                button.clicked.connect(self._clicked)
                self._layout.addWidget(button)
            self._layout.addWidget(QLabel())

        self._layout.addWidget(QWidget())
        self._layout.setStretch(self._layout.count() - 1, 100)

    def clear(self):
        clear_layout(self._layout)

    def _clicked(self):
        entry, value = self.sender().text().split()
        self.button_clicked.emit(entry, int(value))
