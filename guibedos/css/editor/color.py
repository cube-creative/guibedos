import colorsys
from Qt.QtCore import Signal, Qt
from Qt.QtWidgets import QWidget, QSlider, QGridLayout, QLabel


class Color(QWidget):
    changed = Signal(object, object, object)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.hue = QSlider()
        self.hue.setMaximum(100)
        self.hue.setOrientation(Qt.Horizontal)
        self.hue.valueChanged.connect(self._changed)

        self.saturation = QSlider()
        self.saturation.setMaximum(100)
        self.saturation.setOrientation(Qt.Horizontal)
        self.saturation.valueChanged.connect(self._changed)

        self.value = QSlider()
        self.value.setMaximum(100)
        self.value.setOrientation(Qt.Horizontal)
        self.value.valueChanged.connect(self._changed)

        layout = QGridLayout(self)
        layout.addWidget(QLabel("H"))
        layout.addWidget(QLabel("S"))
        layout.addWidget(QLabel("V"))
        layout.addWidget(self.hue, 0, 1)
        layout.addWidget(self.saturation, 1, 1)
        layout.addWidget(self.value, 2, 1)

    def set_rgb(self, r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        self.hue.setValue(h * 100)
        self.saturation.setValue(s * 100)
        self.value.setValue(v * 100)

    def _changed(self):
        r, g, b = colorsys.hsv_to_rgb(
            self.hue.value() / 100.0,
            self.saturation.value() / 100.0,
            self.value.value() / 100.0,
        )
        self.changed.emit(
            int(r * 255),
            int(g * 255),
            int(b * 255)
        )
