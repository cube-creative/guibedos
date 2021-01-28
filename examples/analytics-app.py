"""
This demonstrates the use of GUI Bedos analytics

```
python -m guidebos.analytics --name AnalyticsDemo --json analytics-demos.json analytics-app.py
```
"""
import logging
from Qt import QtWidgets
from guibedos.helpers import use_case


logging.basicConfig(level=logging.INFO)


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.button_peace = QtWidgets.QPushButton('Ensure world peace')
        self.button_peace.clicked.connect(self.peace_clicked)

        self.button_immortal = QtWidgets.QPushButton('Become immortal')
        self.button_immortal.clicked.connect(self.immortal_clicked)

        self.button_fly = QtWidgets.QPushButton('Learn to fly')
        self.button_fly.clicked.connect(self.fly_clicked)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.button_peace)
        layout.addWidget(self.button_immortal)
        layout.addWidget(self.button_fly)

    @use_case('Ensure world peace')
    def peace_clicked(self):
        print("The world is now a peaceful place")

    @use_case('Become immortal')
    def immortal_clicked(self):
        print("You are now immortal")

    @use_case('Learn to fly')
    def fly_clicked(self):
        raise RuntimeError("No one can fly")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(800, 150)
    window.show()

    app.exec_()
