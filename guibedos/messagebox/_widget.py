from Qt import QtWidgets


WARNING = QtWidgets.QMessageBox.Icon.Warning
INFO = QtWidgets.QMessageBox.Icon.Information


def make_box(message, title, icon):
    confirmation_box = QtWidgets.QMessageBox(QtWidgets.QApplication.topLevelWidgets()[0])
    confirmation_box.setIcon(icon)
    confirmation_box.setWindowTitle(title)
    confirmation_box.setText(message)
    confirmation_box.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

    result = confirmation_box.exec_() == QtWidgets.QMessageBox.Ok
    confirmation_box.deleteLater()

    return result
