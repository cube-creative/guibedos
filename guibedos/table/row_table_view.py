from Qt.QtCore import Qt, QMargins
from Qt.QtWidgets import QTableView, QAbstractItemView, QStyledItemDelegate
from .row_table_model import RowTableModel


CELL_PADDING = 8


class CellDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        return QStyledItemDelegate.sizeHint(self, option, index).grownBy(
            QMargins(CELL_PADDING, CELL_PADDING, CELL_PADDING, CELL_PADDING
        ))


class RowTableView(QTableView):

    def __init__(self,
        auto_resize=False,
        single_row_select=True,
        context_menu_callback=None,
        last_column_stretch=False,
        parent=None
    ):
        QTableView.__init__(self, parent)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setSelectionMode(
            QAbstractItemView.SingleSelection if single_row_select
            else QAbstractItemView.ExtendedSelection
        )
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.horizontalHeader().setStretchLastSection(last_column_stretch)
        self.verticalHeader().hide()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setHorizontalScrollMode(QTableView.ScrollPerPixel)
        self.setItemDelegate(CellDelegate())

        self.verticalHeader().setDefaultSectionSize(self.verticalHeader().defaultSectionSize() + CELL_PADDING)

        if context_menu_callback is not None:
            self.customContextMenuRequested.connect(context_menu_callback)

        self._auto_resize = auto_resize
        self._single_row_select = single_row_select
        self._model = None

    def setModel(self, model):
        if not isinstance(model, RowTableModel):
            raise TypeError("Given model must be a RowTableModel")

        QTableView.setModel(self, model)
        self._model = model

        if self._auto_resize:
            self._model.modelReset.connect(self.resizeRowsToContents)
            self._model.modelReset.connect(self.resizeColumnsToContents)
            self.resizeColumnsToContents()
            self.resizeRowsToContents()
