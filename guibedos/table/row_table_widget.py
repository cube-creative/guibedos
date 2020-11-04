"""
This demonstrates the usage of a QTableView associated width a QAbstractTableModel

Presented data is organized in rows
"""
from Qt.QtCore import Signal, Qt
from PySide2.QtWidgets import QGridLayout, QLineEdit, QProgressBar, QPushButton, QLabel, QFrame
from .row_table_view import RowTableView
from guibedos.helpers import Hourglass


SEARCHBAR_HEIGHT = 24
STATUS_LABEL_WIDTH = 150
STATUS_LABEL_MESSAGE = "{} rows ({} total)"


class RowTableWidget(QFrame):
    double_clicked = Signal(object)

    def __init__(self,
        auto_resize=False,
        single_row_select=True,
        context_menu_callback=None,
        last_column_stretch=True,
        parent=None
    ):
        QFrame.__init__(self, parent)
        self.model = None

        self.table_view = RowTableView(auto_resize, single_row_select, context_menu_callback, last_column_stretch)
        self.table_view.doubleClicked.connect(self._double_clicked)

        self.search_bar = QLineEdit()
        self.search_bar.setFixedHeight(SEARCHBAR_HEIGHT)
        self.search_bar.textChanged.connect(self.set_search_text)
        self.search_bar.setToolTip("Search bar")

        self.auto_size_button = QPushButton('<>')
        self.auto_size_button.setFixedSize(SEARCHBAR_HEIGHT, SEARCHBAR_HEIGHT)
        self.auto_size_button.clicked.connect(self._auto_size_clicked)
        self.auto_size_button.setToolTip("Auto size")

        self.status_label = QLabel(STATUS_LABEL_MESSAGE.format(0, 0))
        self.status_label.setFixedWidth(STATUS_LABEL_WIDTH)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat('')

        layout = QGridLayout()
        #layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.search_bar, 0, 0, 1, 2)
        layout.addWidget(self.auto_size_button, 0, 2)
        layout.addWidget(self.table_view, 1, 0, 1, 3)
        layout.addWidget(self.status_label, 2, 0)
        layout.addWidget(self.progress_bar, 2, 1, 1, 2)
        layout.setColumnStretch(1, 100)

        self.setLayout(layout)

    def set_model(self, model):
        self.model = model
        self.table_view.setModel(model)
        model.modelReset.connect(self._set_progress_maximum)
        model.modelReset.connect(self._update_status)
        model.progress_updated.connect(self._update_progress)

        self._set_progress_maximum()
        self._update_status()
        self.progress_bar.setVisible(model.has_background_callback)

    @property
    def search_text(self):
        return self.search_bar.text()

    def set_search_text(self, text):
        self.search_bar.blockSignals(True)
        self.search_bar.setText(text)
        self.search_bar.blockSignals(False)
        self.model.set_search_text(text)

    def _set_progress_maximum(self):
        self.progress_bar.setMaximum(self.model.progress_max)  # do better ?

    def _update_progress(self, value):
        self.progress_bar.setValue(value)

    def _update_status(self):
        self.status_label.setText(STATUS_LABEL_MESSAGE.format(
            self.model.rowCount(), self.model.total_row_count
        ))

    def _auto_size_clicked(self):
        with Hourglass():
            self.table_view.resizeColumnsToContents()
            self.table_view.resizeRowsToContents()

    def _double_clicked(self, index):
        row = self.model.data(index, Qt.UserRole)
        self.double_clicked.emit(row)

    def state(self):
        header_sizes = list()
        header = self.table_view.horizontalHeader()
        for section_index in range(header.count()):
            header_sizes.append(header.sectionSize(section_index))

        return {
            'header_sizes': header_sizes,
            'search_text': self.search_bar.text()
        }

    def load_state(self, state):
        header = self.table_view.horizontalHeader()
        for section_index, size in enumerate(state['header_sizes']):
            header.resizeSection(section_index, size)

        self.search_bar.setText(state['search_text'])
