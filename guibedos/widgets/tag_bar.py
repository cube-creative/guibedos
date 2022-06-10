"""
Button based LineEdit, for tag edition
"""
import re

try:
    from Qt import QtWidgets
    from Qt import QtCore
except ImportError:
    from qtpy import QtWidgets
    from qtpy import QtCore

from ..css import parse_images
from .flow_layout import FlowLayout


_REGEXP = re.compile(r'<tag:([^>]+)>')


class Clipboard(object):
    """
    Thin wrapper around QApplication's clipboard
    """

    @staticmethod
    def get():
        clipboard = QtWidgets.QApplication.clipboard()
        return clipboard.text()

    @staticmethod
    def set(text_):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(text_)


class _ButtonSelectionModel(object):
    def __init__(self):
        self._names = list()
        self._index = 0
        self._shift_index = 0
        self._is_shift = False

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, names):
        self._names = names
        self._index = 0
        self._shift_index = 0

    @property
    def current(self):
        """
        Name of the selected Button (active)
        :return:
        """
        return self.names[self._index]

    def _update_shift(self, is_shift=False):
        """
        Checks whether shift status has changed, then stores the index at which shift was pressed
        :param is_shift: Shift status
        """
        if self._is_shift != is_shift:
            self._shift_index = self._index

        self._is_shift = is_shift

    def desselect(self):
        self._index = 0
        self._shift_index = 0
        self._is_shift = False

    def left(self, is_shift=False):
        """
        Move selection one step left
        :param is_shift: if shift key is pressed
        """
        self._update_shift(is_shift)
        self._index = max(self._index - 1, -len(self.names))

    def right(self, is_shift=False):
        """
        Move selection one step right
        :param is_shift: if shift key is pressed
        """
        self._update_shift(is_shift)
        self._index = min(0, self._index + 1)

    def selected(self):
        """
        Names of the selected Buttons
        :return:
        """
        if self._is_shift:
            if self._index == self._shift_index:
                return [self.names[self._index]]

            elif self._index < self._shift_index:
                self._shift_index = min(-1, self._shift_index)
                indexes = range(self._index, self._shift_index + 1)
                return [self.names[i] for i in indexes]

            else:
                self._index = min(-1, self._index)
                indexes = range(self._shift_index, self._index + 1)
                return [self.names[i] for i in indexes]

        if self._index == 0:
            return list()

        return [self.names[self._index]]


class TagBar(QtWidgets.QWidget):
    STYLE_SHEET = """
    QPushButton {
        padding: 3px 17px 3px 8px;
        margin: 0px 0px;
        background-image: url(qss:images/close_light.png);
        background-position: right;
        background-repeat: none;
    }
    
    QComboBox:editable {
        color : #5a5a5a;
        background-color: #cbd8e6;
        padding: 0px 0px 2px 0px;
    }
    
    QComboBox QAbstractItemView {
        color : #5a5a5a;
    }
    """
    tags_changed = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(TagBar, self).__init__(parent=parent)
        self.setStyleSheet(parse_images(self.STYLE_SHEET))
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self._model = _ButtonSelectionModel()
        self._buttons = list()

        self._autocompletables = list()

        self._editor = QtWidgets.QComboBox()
        self._editor.name = "-#-#-EDITOR-#-#-"
        self._editor.currentIndexChanged.connect(self._index_changed)
        self._editor.setEditable(True)
        self._editor.installEventFilter(self)

        self._layout = FlowLayout(self, expand_last=(True, False))
        self._layout.addWidget(self._editor)

    @property
    def tags(self):
        return [button.name for button in self._buttons]

    @property
    def autocompletables(self):
        return self._autocompletables

    @autocompletables.setter
    def autocompletables(self, items):
        self._autocompletables = items
        completer = QtWidgets.QCompleter(self._autocompletables, self)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._editor.blockSignals(True)
        self._editor.setCompleter(completer)
        self._editor.clear()
        self._editor.addItems(items)
        self._editor.blockSignals(False)
        self._editor.setCurrentIndex(-1)

    def _index_changed(self):
        """
        When a choice is made in the combobox
        """
        self.add_button_from_text()

    def _update_model(self):
        """
        Updates model with current button names
        """
        self._model.names = [button.name for button in self._buttons]

    def _new_button(self, tag):
        """
        Creates a new widget button
        :param tag: A valid tag
        :return: the new QPushButton, None otherwise
        """
        if tag in self._model.names:
            return

        if '<' in tag or '>' in tag or not tag:
            return

        button = QtWidgets.QPushButton(tag)
        button.clicked.connect(self._button_clicked)
        button.setFocusPolicy(QtCore.Qt.NoFocus)
        button.installEventFilter(self)
        button.name = tag

        self._layout.insertWidget(self._layout.count() - 1, button)
        self._buttons.append(button)
        self._update_model()

        self.tags_changed.emit(self.tags)

        return button

    def _button_clicked(self):
        """
        Deletes button when clicked
        """
        self._delete_button(self.sender().name)

    def _set_text_editable(self, is_enabled):
        """
        Defines if text edit is editable
        :param is_enabled: bool
        """
        self._editor.lineEdit().setReadOnly(not is_enabled)

    def _set_text_cursor_position(self, position):
        """
        Defines cursor position of text edit
        :param position: int
        """
        self._editor.lineEdit().setCursorPosition(position)

    def _select_buttons(self):
        """
        Updates buttons states according to model
        """
        _ = [button.setDown(False) for button in self._buttons]

        for name in self._model.selected():
            index = self._model.names.index(name)
            button = self._buttons[index]
            button.setDown(True)

    def _delete_button(self, name):
        """
        Deletes a button by its name
        :param name: Button name
        """
        index = [item.widget().name for item in self._layout.item_list].index(name)
        if self._layout.removeAt(index) is not None:
            self._buttons.pop(index)

        self._update_model()

        self.tags_changed.emit(self.tags)

    def _delete_selected_buttons(self):
        """
        Removes selected buttons
        """
        names = self._model.selected()

        # TODO : this should be dealt with by caller !!
        if not names:
            names = [self._model.names[-1]]

        for name in names:
            self._delete_button(name)

    def desselect(self):
        """
        Clears button selection
        """
        self._model.desselect()
        self._select_buttons()

    def add_button_from_text(self):
        """
        Adds a new button, according to editable text content, clears text editor
        """
        text = self._editor.currentText()
        self._new_button(text)

        self._editor.blockSignals(True)
        self._editor.setEditText('')
        self._editor.blockSignals(False)

    def set_tags(self, tags):
        """
        Clears buttons and sets them
        :param tags: list of str
        """
        for name in self._model.names:
            self._delete_button(name)

        for name in tags:
            self._new_button(name)

    def eventFilter(self, object_, event):
        type_ = event.type()
        text = self._editor.currentText()
        cursor = self._editor.lineEdit().cursorPosition()
        text_selected = self._editor.lineEdit().selectedText()
        is_shift = QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ShiftModifier == QtCore.Qt.ShiftModifier
        is_ctrl = QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier

        if type_ == QtCore.QEvent.KeyPress:
            key = event.key()

            # TODO : better unification with model._delete_selected_buttons()
            if key == QtCore.Qt.Key_Backspace and cursor == 0 and self._buttons and not text_selected:
                self._delete_selected_buttons()

            if key == QtCore.Qt.Key_Delete and self._model.selected():
                self._delete_selected_buttons()

            elif key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return) and text:
                self.add_button_from_text()
                return True

            elif key == QtCore.Qt.Key_Left and cursor == 0 and self._buttons:
                self._model.left(is_shift)
                self._select_buttons()
                return True

            elif key == QtCore.Qt.Key_Right and cursor == 0:
                self._model.right(is_shift)
                self._select_buttons()
                return bool(self._model.selected())

            elif key == QtCore.Qt.Key_C and is_ctrl:
                tags = ' '.join(['<tag:{}>'.format(tag) for tag in self._model.selected()])
                Clipboard.set(tags)
                self.desselect()
                return True

            elif key == QtCore.Qt.Key_V and is_ctrl:
                for tag in _REGEXP.findall(Clipboard.get()):
                    self._new_button(tag)
                self.desselect()
                return True

            elif key == QtCore.Qt.Key_Tab:
                parent = self.parent()
                if parent: parent.focusNextChild()

            elif key == QtCore.Qt.Key_Backtab:
                parent = self.parent()
                if parent: parent.focusPreviousChild()

        return QtWidgets.QWidget.eventFilter(self, object_, event)
