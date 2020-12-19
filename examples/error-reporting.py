from Qt import QtWidgets
from guibedos import css
from guibedos.error_reporting import error_reported


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.button_normal = QtWidgets.QPushButton('Normal Button')
        self.button_normal.clicked.connect(self.button_normal_clicked)

        self.button_raising = QtWidgets.QPushButton('Error raising Button')
        self.button_raising.clicked.connect(self.button_raising_clicked)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.button_normal)
        layout.addWidget(self.button_raising)

    @error_reported('Normal Clicked')
    def button_normal_clicked(self):
        print("Normal button clicked")

    @error_reported('Raising demonstration')
    def button_raising_clicked(self):
        raise RuntimeError('An exception has occurred')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(800, 150)
    window.show()

    app.exec_()
