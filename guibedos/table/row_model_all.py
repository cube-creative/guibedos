from PySide2.QtCore import QObject, Signal, QCoreApplication
from guibedos.threading import move_to_new_thread
from .row_background_processor import RowBackgroundProcessor


class RowAllModel(QObject):
    """
    This class holds all the rows set with `set_rows` and ensure background processing if a callback is provided
    """
    row_updated = Signal(object)
    progress_updated = Signal(int)

    def __init__(self, background_processing_callback=None, parent=None):
        QObject.__init__(self, parent)
        self.rows = list()
        self.row_count = 0

        self._processed_row_indexes = list()
        self._background_processor = RowBackgroundProcessor()
        self._background_thread = move_to_new_thread(
            self._background_processor,
            signals=[
                (self._background_processor.row_processed, self.update_row)
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

    def add_row_for_processing(self, row):
        if self.has_background_callback and row.index not in self._processed_row_indexes:
            self._background_processor.add_row(row)

    def update_row(self, row):
        self._processed_row_indexes.append(row.index)
        self.rows[row.index] = row
        self.row_updated.emit(row)
        self.progress_updated.emit(len(self._processed_row_indexes))

    def set_rows(self, rows):
        self.rows = list()
        self._processed_row_indexes = list()
        self._background_processor.reset()

        for index, row in enumerate(rows):
            new_row = row.copy(new_index=index)
            new_row.build_cache()
            self.rows.append(new_row)
            if self._background_processor.has_callback:
                self._background_processor.add_row(new_row)

        self.row_count = len(self.rows)
