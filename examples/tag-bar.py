from Qt import QtWidgets
from guibedos import css
from guibedos.widgets import TagBar


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.one = TagBar()
        self.one.autocompletables = ['Layout', 'Buildings', 'Characters', 'Animation']
        self.two = TagBar()

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QtWidgets.QLabel("TagBar 1 :"), 0, 0)
        layout.addWidget(self.one, 0, 1)
        layout.addWidget(QtWidgets.QLabel("TagBar 2 :"), 1, 0)
        layout.addWidget(self.two, 1, 1)
        layout.addWidget(QtWidgets.QWidget(), 2, 0)
        layout.setColumnStretch(1, 100)
        layout.setRowStretch(2, 100)

        self.one.set_tags(['Modeling', 'Vegetation', 'Scatterable'])
        self.two.set_tags(['Flowers'])


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    css.set_theme(app, 'dark-blue')

    window = Window()
    window.resize(800, 150)
    window.show()

    print(window.one.tags)
    print(window.two.tags)

    app.exec_()
