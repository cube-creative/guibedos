import functools
import traceback

from PySide2.QtGui import QFontDatabase, QFont
from PySide2.QtWidgets import QDialog, QPlainTextEdit, QLabel, QGridLayout,QApplication, QStyle, QPushButton

from .highlighter import TracebackHighlighter


ICON_SIZE = 48

# http://srinikom.github.io/pyside-docs/PySide/QtGui/QStyle.html#PySide.QtGui.PySide.QtGui.QStyle.StandardPixmap


class _ReportingWindow(QDialog):
    def __init__(self, name, report, parent=None):
        QDialog.__init__(self, parent)
        icon = self.style().standardIcon(QStyle.SP_MessageBoxCritical)

        self.setWindowTitle('Error reporting')
        self.setWindowIcon(icon)

        font = QFontDatabase().systemFont(QFontDatabase.FixedFont)

        self.text = QPlainTextEdit()
        self.text.setFont(font)
        self.text.setReadOnly(True)
        self.text.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.text.setPlainText(report)
        TracebackHighlighter(self.text.document())

        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(ICON_SIZE, ICON_SIZE))

        label = QLabel("{} error !".format(name))
        label.setFont(QFont('default', pointSize=14))

        button_copy = QPushButton('Copy to clipboard')
        button_copy.clicked.connect(self._copy)

        layout = QGridLayout(self)
        layout.addWidget(icon_label, 0, 0)
        layout.addWidget(label, 0, 1)
        layout.addWidget(self.text, 1, 0, 1, 2)
        layout.addWidget(button_copy, 2, 0, 1, 2)
        layout.setColumnStretch(1, 100)

        self.setModal(True)
        self.resize(600, 400)

    def _copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText('```\n' + self.text.toPlainText() + '\n```')


def error_reported(name):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)
            except Exception as e:
                window = _ReportingWindow(
                    name,
                    traceback.format_exc(),
                    parent=QApplication.activeWindow()
                )
                window.show()

                raise

        return wrapper
    return decorator
