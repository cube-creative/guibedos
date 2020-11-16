import re

from Qt.QtGui import QFont
from Qt.QtCore import Signal
from Qt.QtWidgets import QTabWidget, QPlainTextEdit

from .highlighter import TemplateHighlighter


RE_TABS = re.compile(r'^\/\*([^\/\*]+)\*\/$', re.MULTILINE)
DEFAULT_TAB = "CSS"


class CSSTextEdit(QTabWidget):
    changed = Signal()

    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)

        self._font = QFont('monospace')
        self._texts = dict()
        self._widgets_indexes = dict()

        self.new_tab(DEFAULT_TAB, '')

    def clear(self):
        QTabWidget.clear(self)
        self._texts = dict()
        self._widgets_indexes = dict()

    def new_tab(self, title, text):
        new_editor = QPlainTextEdit()
        new_editor.setFont(self._font)
        new_editor.setPlainText(text)
        TemplateHighlighter(new_editor.document())

        new_editor.textChanged.connect(self._text_changed)
        self._widgets_indexes[new_editor] = self.count()
        self.addTab(new_editor, title)

    def set_plain_text(self, text):
        self.clear()

        if not text:
            self.new_tab(DEFAULT_TAB, '')
            return

        items = iter(RE_TABS.split(text))
        for item in items:
            if not item:
                continue

            tab_name = item.strip()
            tab_text = next(items).strip()

            self._texts[tab_name] = tab_text
            self.new_tab(tab_name, tab_text)

    def plain_text(self):
        texts = list()
        for name, text in self._texts.items():
            if not text:
                continue

            texts.append('/* {} */'.format(name))
            texts.append(text)
            texts.append("")

        return '\n'.join(texts)

    def _text_changed(self, *args):
        text_edit = self.sender()
        text = text_edit.toPlainText()
        tab_name = self.tabBar().tabText(self._widgets_indexes[self.sender()])

        self._texts[tab_name] = text

        if RE_TABS.findall(text):
            whole_text = self.plain_text()
            self.set_plain_text(whole_text)

        self.changed.emit()
