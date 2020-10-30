from PySide2.QtGui import QColor


class Row:
    """
    Holds data for a table row

    Each cell is a list of list as of this schema

    ```text
    [Display role, foreground color, background color]
    ```

    Color are a 0-255 RGB/RGBA tuple `(0, 255, 128)` or `(0, 255, 128, 128)`

    :cells: list of tuples
    :data: user data, not displayed
    """
    DISPLAY = 0
    BACKGROUND = 1
    FOREGROUND = 2
    SORT = 3

    def __init__(self, cells, data, index=-1):
        self.index = index
        self.data = data
        self.cells = cells
        self.search_cache = ""

    def copy(self, new_index=None):
        if new_index is None:
            new_index = self.index

        return Row(self.cells, self.data, new_index)

    def build_cache(self):
        self.search_cache = " ".join('{}'.format(cell[Row.DISPLAY]).lower() for cell in self.cells)
        self.cells = [self._cell_cache(cell) for cell in self.cells]

    @staticmethod
    def _cell_cache(cell):
        display = cell[Row.DISPLAY]
        foreground = Row._ensure_qcolor(cell[Row.FOREGROUND])
        background = Row._ensure_qcolor(cell[Row.BACKGROUND])
        sort = cell[Row.SORT] if cell[Row.SORT] is not None else 0
        return [display, background, foreground, sort]

    @staticmethod
    def _ensure_qcolor(value):
        if not value:
            return None
        elif not isinstance(value, QColor):
            return QColor(*value)
        return value

    def __repr__(self):
        return "<Row(index={}, cells={})>".format(
            self.index,
            self.cells
        )
