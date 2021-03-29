from Qt import QtWidgets

from guibedos.messagebox import before


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.button_info = QtWidgets.QPushButton('Information before')
        self.button_info.clicked.connect(self.button_info_clicked)

        self.button_warning = QtWidgets.QPushButton('Warning before')
        self.button_warning.clicked.connect(self.button_warning_clicked)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.button_info)
        layout.addWidget(self.button_warning)

    @before.info('You are about to do something')
    def button_info_clicked(self):
        print("Something just happened")

    @before.warning('Attention ! You are about to do something !')
    def button_warning_clicked(self):
        print("Wow ! Something just happened !")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(800, 150)
    window.show()

    app.exec_()
