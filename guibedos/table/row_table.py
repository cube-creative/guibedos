"""
This demonstrates the usage of a QTableView associated width a QAbstractTableModel

Presented data is organized in rows
"""
from Qt.QtGui import QColor
from Qt.QtCore import Qt, QAbstractTableModel, Signal, QThread
from Qt.QtWidgets import QTableView, QAbstractItemView
from guibedos.threading import Threadable, move_to_new_thread


class Row:
    def __init__(self, cells, data, index=-1):
        self.index = index
        self.data = data
        self.cells = cells


class RowTable(QTableView):

    def __init__(self,
        auto_resize=False,
        single_row_select=True,
        context_menu_callback=None,
        last_column_stretch=True,
        parent=None
    ):
        QTableView.__init__(self, parent)
        self.setSortingEnabled(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setSelectionMode(
            QAbstractItemView.SingleSelection if single_row_select
            else QAbstractItemView.ExtendedSelection
        )
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.horizontalHeader().setStretchLastSection(False)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.verticalHeader().hide()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().setStretchLastSection(last_column_stretch)

        if context_menu_callback is not None:
            self.customContextMenuRequested.connect(context_menu_callback)

        self._auto_resize = auto_resize
        self._single_row_select = single_row_select

    def setModel(self, model):
        if not isinstance(model, RowTableModel):
            raise TypeError("Given model must be a RowTableModel")

        QTableView.setModel(self, model)
        if self._auto_resize:
            self.model().modelReset.connect(self.resizeColumnsToContents)
            self.resizeColumnsToContents()

    def resizeColumnsToContents(self):
        QTableView.resizeColumnsToContents(self)
        self.model().reset_background_processing()

    def closeEvent(self, event):
        self.model().stop()
        event.accept()


class RowBackgroundProcessor(Threadable):
    row_processed = Signal(object)

    def __init__(self, parent=None):
        Threadable.__init__(self, parent)
        self._rows = list()
        self._process_callback = None
        self._processed_row_indexes = list()

    @property
    def has_callback(self):
        return self._process_callback is not None

    def set_callback(self, callback):
        self._process_callback = callback

    def reset(self):
        self._rows = list()
        self._processed_row_indexes = list()

    def add_row(self, row):
        self._rows.append(row)

    def loop_kick(self):
        if not self._rows:
            QThread.msleep(self.DEFAULT_SLEEP_MS)
            return

        row = self._rows.pop()
        if row.index not in self._processed_row_indexes:
            self.row_processed.emit(self._process_callback(row))
            self._processed_row_indexes.append(row.index)

        self._remove_already_loaded()

        QThread.msleep(20)

    def _remove_already_loaded(self):
        for row in reversed(self._rows):
            if row.index in self._processed_row_indexes:
                self._rows.pop()


class RowTableModel(QAbstractTableModel):
    DISPLAY = 0
    BACKGROUND = 1
    FOREGROUND = 2
    _ROLES = {
        Qt.DisplayRole: DISPLAY,
        Qt.BackgroundRole: BACKGROUND,
        Qt.ForegroundRole: FOREGROUND
    }

    def __init__(self, background_processing_callback=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._headers = list()
        self._rows = list()
        self._row_count = 0
        self._column_count = 0

        self._processed_row_indexes = list()
        self._background_processor = RowBackgroundProcessor()
        self._background_thread = move_to_new_thread(
            self._background_processor,
            signals=[
                (self._background_processor.row_processed, self.row_processed)
            ]
        )
        self.set_background_processing_callback(background_processing_callback)

    def reset_background_processing(self):
        self._background_processor.reset()
        self._processed_row_indexes = list()

    def set_background_processing_callback(self, callback):
        self._background_processor.set_callback(callback)

    def start(self):
        self._background_thread.start()

    def stop(self):
        self._background_processor.stop()

    @staticmethod
    def precompute_cell(cell):
        background = QColor(*cell[1]) if cell[1] else None
        foreground = QColor(*cell[2]) if cell[2] else None
        return [cell[0], background, foreground]

    def row_processed(self, row):
        self._processed_row_indexes.append(row.index)
        self._rows[row.index] = row
        self.dataChanged.emit(
            self.index(row.index, 0),
            self.index(row.index, self._column_count)
        )

    def set_headers(self, headers):
        if headers:
            self._headers = headers
            self._column_count = len(self._headers)
        else:
            self._headers = list()
            self._column_count = 0

    def set_rows(self, rows):
        if rows:
            self._rows = list()
            self._background_processor.reset()
            self._processed_row_indexes = list()

            for index, row in enumerate(rows):
                new_row = Row(
                    cells=[self.precompute_cell(cell) for cell in row.cells],
                    data=row.data,
                    index=index
                )
                self._rows.append(new_row)

            self._row_count = len(rows)

        else:
            self._rows = list()
            self._background_processor.reset()
            self._processed_row_indexes = list()

            self._row_count = 0

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

        if role == Qt.DisplayRole and \
                self._background_processor.has_callback and \
                row_index not in self._processed_row_indexes:
            self._background_processor.add_row(self._rows[row_index])

        data_type = self._ROLES.get(role)
        if data_type is None:
            return

        return self._rows[row_index].cells[column_index][data_type]
