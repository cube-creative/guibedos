"""
This demonstrates the usage of a QTableView associated width a QAbstractTableModel

Presented data is organized in rows
"""
import random
from Qt.QtWidgets import QApplication
from guibedos.table import Row, RowTable, RowTableModel


def make_data():
    rows = list()
    colors = [None, (0, 255, 255), (255, 255, 0), (255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
    words = ["Word", "War", "Why", "Jambon", "Beurre", "Pomme", "Lenalol", "Pulene"]

    for i in range(1000):
        rows.append(Row([
            (random.choice(words), None, None),  # cell column 0
            (random.choice(words), random.choice(colors), None),  # cell column 1
            (random.choice(words), None, None),  # cell column 2
            (random.choice(words), None, random.choice(colors)),  # cell column 3
            ('...', None, None)  # cell column 4, will be computed in background
        ], {
            "random_word": random.choice(words)
        }
        ))

    return rows


def process_row(row):
    row.cells[0][0] += ' <'
    row.cells[4] = RowTableModel.precompute_cell((
        'PROCESSED : {}'.format(row.data),
        None,
        (255, 0, 0)
    ))

    return row


if __name__ == '__main__':
    app = QApplication([])
    vue = RowTable(
        auto_resize=False,
        single_row_select=True,
        context_menu_callback=None
    )

    model = RowTableModel(
        background_processing_callback=process_row
    )
    model.set_headers(['Header', 'are', 'set', 'here', 'Computed data here'])
    model.set_rows(make_data())
    model.start()

    vue.setModel(model)

    vue.resize(1280, 720)
    vue.show()

    app.exec_()
