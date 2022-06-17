"""
Allows to use Qt.py inside Blender

!!! warning
    **Do not use** `QApplication.exec_()` as it will block Blender's main loop

See `tube_scenemanager`, `character_picker` and `resource_library` for examples
"""
import atexit

try:
    from Qt import QtWidgets
    from Qt import QtCore
except ImportError:
    from qtpy import QtWidgets
    from qtpy import QtCore

from . import css
import bpy
from bpy.app.handlers import persistent


_CSS_THEME = 'dark-blue'
_CSS_CENTRAL_STYLE = """
background-color: #8c8c8c;
background-image: url(qss:images/background_mdi.png);
background-position: center center;
"""
_theme_set = False
_main_window = None
_application = None
_widgets = list()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowTitle("GUI Bedos : Blender")
        self.resize(800, 700)
        self.setDockNestingEnabled(True)

        central = QtWidgets.QLabel()
        central.setStyleSheet(css.parse_images(_CSS_CENTRAL_STYLE))
        self.setCentralWidget(central)

        self.closed = False

        self.settings = QtCore.QSettings('GUIBedos', 'Blender')
        geometry = self.settings.value('geometry', '')
        if geometry:
            self.restoreGeometry(geometry)

    def save_geometry(self):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)

    def closeEvent(self, event):
        for dock in self.findChildren(QtWidgets.QDockWidget):
            dock.close()

        self.closed = True

        self.save_geometry()

        return QtWidgets.QMainWindow.closeEvent(self, event)

    def event(self, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            for dock in self.findChildren(QtWidgets.QDockWidget):
                #dock.activate()
                pass

        return QtWidgets.QMainWindow.event(self, event)


class Dockable(QtWidgets.QDockWidget):
    """
    QDockWidget that wraps a given QWidget so it can be docked in MainWindow
    """
    def __init__(self, wrapped_widget, parent=None):
        QtWidgets.QDockWidget.__init__(self, parent)
        self.wrapped_widget = wrapped_widget
        self.setWidget(self.wrapped_widget)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable | QtWidgets.QDockWidget.DockWidgetMovable)
        self.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.setWindowTitle(self.wrapped_widget.windowTitle())

    def closeEvent(self, event):
        self.wrapped_widget.close()
        return QtWidgets.QDockWidget.closeEvent(self, event)


@atexit.register
def save_mainwindow_geometry():
    """
    Saves main window's geometry before exiting
    """
    global _main_window

    if _main_window is None or _main_window.closed:
        return

    _main_window.save_geometry()


def ensure_qapplication():
    """
    Ensures that a QApplication instance exists
    """
    global _application, _theme_set

    if _application is not None:
        return _application

    _application = QtWidgets.QApplication.instance()
    if _application is None:
        _application = QtWidgets.QApplication([])

    if not _theme_set:
        css.set_theme(_application, _CSS_THEME)
        _theme_set = True

    return _application


def ensure_main_window():
    global _main_window

    if _main_window is None or _main_window.closed:
        _main_window = MainWindow()
        _main_window.show()

    return _main_window


@persistent
def _event_loop_kick(dummy):
    if QtCore.QEventLoop().isRunning():
        QtCore.QEventLoop().processEvents()


def ensure_event_loop():
    """
    Ensures that the QEventLoop handler is registered in Blender's main loop
    """
    if _event_loop_kick not in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.append(_event_loop_kick)


def prevent_deletion(widget):
    """
    Registers a widget to prevent its garbage collection

    :param widget: an instance of any subclass of QWidget
    """
    global _widgets
    if widget not in _widgets:
        _widgets.append(widget)


def new_widget(widget_class, *args, **kwargs):
    """
    Creates an instance of the given widget class and returns it

    Also ensures a QApplication exists, and it's QLoopEvent is handled by a Blender handler

    :param widget_class: class of the widget (any subclass of QWidget)
    :param args: positional arguments for widget creation
    :param kwargs: named arguments for widget creation
    :return: the newly created widget
    """
    # TODO : Cleanup _widgets using https://shiboken.readthedocs.io/en/latest/shibokenmodule.html
    ensure_qapplication()
    new_widget = widget_class(*args, **kwargs)
    prevent_deletion(new_widget)
    ensure_event_loop()

    return new_widget


def dock_to_main_window(widget):
    """
    Wraps the given widget into a QDockWidget and docks it to the QMainWindow
    """
    main_window = ensure_main_window()
    dockable = Dockable(widget)

    if main_window.height() < widget.height():
        main_window.resize(main_window.width(), widget.height())

    main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockable)
    dockable.show()
