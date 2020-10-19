

class Row:
    """
    Holds data for a table row

    Each cell is a list of list as of this schema

    ```text
    [Display role, foreground color, background color]
    ```

    Color are a 0-255 3-items tuple `(0, 255, 128)`

    :cells: list of tuples
    :data: user data, not displayed
    """
    def __init__(self, cells, data, index=-1):
        self.index = index
        self.data = data
        self.cells = cells
        self.search_cache = ""

        self._build_cache()

    def _build_cache(self):
        self.search_cache = " ".join('{}'.format(cell[0]) for cell in self.cells)
