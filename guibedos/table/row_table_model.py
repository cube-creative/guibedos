from PySide2.QtCore import Qt, QAbstractTableModel, Signal, QThread, QCoreApplication
from guibedos.threading import Threadable, move_to_new_thread


class RowBackgroundProcessor(Threadable):
    SLEEP_MS = 20
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
            new_row = self._process_callback(row)
            new_row.build_cache()

            self.row_processed.emit(new_row)
            self._processed_row_indexes.append(new_row.index)

            self._cleanup(row)

        QThread.msleep(self.SLEEP_MS)

    def _cleanup(self, row):
        while True:
            try:
                self._rows.remove(row)
            except ValueError:
                break


class RowTableModel(QAbstractTableModel):
    DISPLAY = 0
    BACKGROUND = 1
    FOREGROUND = 2
    _ROLES = {
        Qt.DisplayRole: DISPLAY,
        Qt.BackgroundRole: BACKGROUND,
        Qt.ForegroundRole: FOREGROUND
    }
    progress_updated = Signal(int)

    def __init__(self, background_processing_callback=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._headers = list()
        self._rows = list()
        self._row_count = 0
        self._column_count = 0

        self._search_text = ""

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

    @property
    def has_background_callback(self):
        return self._background_processor.has_callback

    def start(self):
        self._background_thread.start()
        QCoreApplication.instance().aboutToQuit.connect(self.stop)

    def stop(self):
        self._background_processor.stop()

    def row_processed(self, row):
        self._processed_row_indexes.append(row.index)
        self._rows[row.index] = row
        self.dataChanged.emit(
            self.index(row.index, 0),
            self.index(row.index, self._column_count)
        )
        self.progress_updated.emit(len(self._processed_row_indexes))

    def set_headers(self, headers):
        if headers:
            self._headers = headers
            self._column_count = len(self._headers)
        else:
            self._headers = list()
            self._column_count = 0

    def set_rows(self, rows):
        self.beginResetModel()

        self._rows = list()
        self._processed_row_indexes = list()
        self._background_processor.reset()

        for index, row in enumerate(rows):
            new_row = row.copy(new_index=index)
            new_row.build_cache()
            self._rows.append(new_row)
            if self._background_processor.has_callback:
                self._background_processor.add_row(new_row)

        self._row_count = len(self._rows)

        self.endResetModel()

    def set_search_text(self, text):
        self._search_text = text

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
