from Qt.QtWidgets import QTableView, QAbstractItemView
from Qt.QtCore import Qt
from .row_table_model import RowTableModel


class RowTableView(QTableView):

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
