import sys
import traceback
from PySide2.QtCore import Signal, QThread
from guibedos.threading import Threadable


class RowBackgroundProcessor(Threadable):
    SLEEP_MS = 40
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
            try:
                new_row = self._process_callback(row)
            except Exception as e:
                traceback.print_exception(*sys.exc_info())

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
