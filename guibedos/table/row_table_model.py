from collections import Counter
from Qt.QtCore import Qt, QAbstractTableModel, Signal
from .row import Row
from .row_model_all import RowAllModel


class RowTableModel(QAbstractTableModel):
    """
    This is the actual `QAbstractTableModel` that wraps its `AllRowTableModel` member and allows fast text search
    """
    progress_updated = Signal(int)

    _ROLES = {
        Qt.DisplayRole: Row.DISPLAY,
        Qt.BackgroundRole: Row.BACKGROUND,
        Qt.ForegroundRole: Row.FOREGROUND
    }

    def __init__(self, background_processing_callback=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._model_all = RowAllModel(background_processing_callback)
        self._model_all.row_updated.connect(self._row_updated)
        self._model_all.progress_updated.connect(self.progress_updated)
        self._rows = list()
        self._row_count = 0
        self._headers = list()
        self._column_count = 0
        self._search_text = ""
        self._search_indexes = dict()
        self._sort_column = None
        self._sort_reversed = False
        self._counters = dict()

    @property
    def total_row_count(self):
        return self._model_all.row_count

    def reset_background_processing(self):
        self._model_all.reset_background_processing()

    def set_background_processing_callback(self, callback):
        self._model_all.set_background_processing_callback(callback)

    @property
    def has_background_callback(self):
        return self._model_all.has_background_callback

    def start(self):
        self._model_all.start()

    def stop(self):
        self._model_all.stop()

    def set_headers(self, headers):
        if headers:
            self._headers = headers
            self._column_count = len(self._headers)
        else:
            self._headers = list()
            self._column_count = 0

    def set_rows(self, rows):
        self._model_all.set_rows(rows)
        self.perform_search()

    def set_search_text(self, text):
        self._search_text = text.lower().split()
        self.perform_search()

    def reset_counters(self):
        for _, counter in self._counters.values():
            counter.clear()

    def perform_search(self):
        self.beginResetModel()
        self.reset_counters()
        self._rows = list()

        for row in self._model_all.rows:
            if any(item not in row.search_cache for item in self._search_text):
                continue

            for index, counter in self._counters.items():
                counter[1].update([row.cells[index][Row.DISPLAY]])

            self._rows.append(row)

        self._sort()

        self._row_count = len(self._rows)
        self.endResetModel()

    @property
    def counters(self):
        return dict(self._counters.values())

    def register_counters(self, column_names):
        self._counters = dict()
        column_indexes = [self._headers.index(column) for column in column_names]
        for column_index in column_indexes:
            self._counters[column_index] = self._headers[column_index], Counter()

    def _row_updated(self, row):
        index = self._search_indexes.get(row.index, -1)
        self.dataChanged.emit(
            self.index(0, index),
            self.index(self._column_count, index)
        )

    @property
    def progress_max(self):
        return self._model_all.row_count

    def rowCount(self, parent=None):
        return self._row_count

    def columnCount(self, parent=None):
        return self._column_count

    def headerData(self, section, orientation=Qt.Horizontal, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]

    def data(self, index, role=Qt.DisplayRole):
        row_index = index.row()
        column_index = index.column()

        if role == Qt.DisplayRole:
            self._model_all.add_row_for_processing(self._rows[row_index])

        elif role == Qt.UserRole:
            return self._rows[row_index]

        data_type = self._ROLES.get(role)
        if data_type is None:
            return

        return self._rows[row_index].cells[column_index][data_type]

    def _build_search_indexes(self):
        self._search_indexes = dict()
        for index, row in enumerate(self._rows):
            self._search_indexes[row.index] = index

    def _sort(self):
        if self._sort_column is None:
            return

        def sort(row):
            return row.cells[self._sort_column][Row.SORT]

        self._rows = sorted(self._rows, key=sort, reverse=self._sort_reversed)
        self._build_search_indexes()

    def sort(self, column, order=Qt.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        self._sort_column = column
        self._sort_reversed = order == Qt.AscendingOrder
        self._sort()
        self.layoutChanged.emit()
