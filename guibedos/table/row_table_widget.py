"""
This demonstrates the usage of a QTableView associated width a QAbstractTableModel

Presented data is organized in rows
"""
from PySide2.QtWidgets import QWidget, QGridLayout, QLineEdit, QProgressBar, QPushButton
from .row_table_view import RowTableView
from guibedos.helpers import Hourglass


SEARCHBAR_HEIGHT = 24


class RowTableWidget(QWidget):
    def __init__(self,
        auto_resize=False,
        single_row_select=True,
        context_menu_callback=None,
        last_column_stretch=True,
        parent=None
    ):
        QWidget.__init__(self, parent)
        self.model = None

        self.table_view = RowTableView(auto_resize, single_row_select, context_menu_callback, last_column_stretch)

        self.search_bar = QLineEdit()
        self.search_bar.setFixedHeight(SEARCHBAR_HEIGHT)
        self.search_bar.textChanged.connect(self._search_text_changed)
        self.search_bar.setToolTip("Search bar")

        self.auto_size_button = QPushButton('<>')
        self.auto_size_button.setFixedSize(SEARCHBAR_HEIGHT, SEARCHBAR_HEIGHT)
        self.auto_size_button.clicked.connect(self._auto_size_clicked)
        self.auto_size_button.setToolTip("Auto size")

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setFormat('')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.search_bar)
        layout.addWidget(self.auto_size_button, 0, 1)
        layout.addWidget(self.table_view, 1, 0, 1, 2)
        layout.addWidget(self.progress_bar, 2, 0, 1, 2)

        self.setLayout(layout)

    def set_model(self, model):
        self.model = model
        self.table_view.setModel(model)
        model.modelReset.connect(self._set_progress_maximum)
        model.progress_updated.connect(self._update_progress)
        self._set_progress_maximum()
        self.progress_bar.setVisible(model.has_background_callback)

    def _search_text_changed(self, text):
        self.model.set_search_text(text)

    def _set_progress_maximum(self):
        self.progress_bar.setMaximum(self.model.progress_max)  # do better ?

    def _update_progress(self, value):
        self.progress_bar.setValue(value)

    def _auto_size_clicked(self):
        with Hourglass():
            self.table_view.resizeColumnsToContents()
            self.table_view.resizeRowsToContents()
