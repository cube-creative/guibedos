"""
This demonstrates the usage of a QTableView associated width a QAbstractTableModel

Presented data is organized in rows
"""
from PySide2.QtWidgets import QWidget, QGridLayout, QLineEdit, QProgressBar
from .row_table_view import RowTableView


class RowTableWidget(QWidget):
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
        self.progress_bar = QProgressBar()

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.search_bar)
        layout.addWidget(self.table_view)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def set_model(self, model):
        self.table_view.setModel(model)
        model.modelReset.connect(self._set_progress_maximum)
        model.progress_updated.connect(self._update_progress)
        self._set_progress_maximum()
        self.progress_bar.setVisible(model.has_background_callback)

    def _search_text_changed(self, text):
        self.table_view.model().set_search_text(text)

    def _set_progress_maximum(self):
        self.progress_bar.setMaximum(self.table_view.model().rowCount())  # do better ?

    def _update_progress(self, value):
        self.progress_bar.setValue(value)
