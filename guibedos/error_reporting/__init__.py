from Qt.QtWidgets import QPlainTextEdit
import functools
import traceback


def error_reported(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:

            # parent = QApplication.topLevelWindows()[0]  # todo : improve this
            window = QPlainTextEdit()
            window.setWindowTitle("Error reporting")
            window.setReadOnly(True)
            window.setPlainText(traceback.format_exc())
            window.resize(800, 600)
            window.show()

            raise

    return wrapper
