"""
This demonstrates the use of GUI Bedos CSS Editor
"""
import logging
from Qt import QtWidgets
from guibedos.css.editor import CSSEditor


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

    def peace_clicked(self):
        print("The world is now a peaceful place")

    def immortal_clicked(self):
        print("You are now immortal")

    def fly_clicked(self):
        raise RuntimeError("No one can fly")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(800, 150)
    window.show()

    # Make sure to instanciate *after* creating the top level widgets
    css_editor = CSSEditor('Demo Project')

    app.exec_()
