"""
This demonstrates the usage of a QTableView associated width a QAbstractTableModel

Presented data is organized in rows
"""
from PySide2.QtWidgets import QWidget, QGridLayout, QLineEdit
from .row_table_view import RowTableView


class RowTable(QWidget):
    def __init__(self,
        auto_resize=False,
        single_row_select=True,
        context_menu_callback=None,
        last_column_stretch=True,
        parent=None
    ):
        QWidget.__init__(self, parent)

        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self._search_text_changed)
        self.table_view = RowTableView(auto_resize, single_row_select, context_menu_callback, last_column_stretch)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.search_bar)
        layout.addWidget(self.table_view)

        self.setLayout(layout)

    def set_model(self, model):
        self.table_view.setModel(model)

    def _search_text_changed(self, text):
        self.table_view.model().set_search_text(text)
