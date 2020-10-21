"""
This demonstrates the usage of a QTableView associated width a QAbstractTableModel

Presented data is organized in rows
"""
import random
from PySide2.QtWidgets import QApplication
from guibedos.table import Row, RowTableModel, RowTableWidget


def process_row(row):
    row.cells[0][0] += ' <'
    row.cells[1][1] = (0, 255, 255, 128)
    row.cells[4] = (
        'PROCESSED : {}'.format(row.data),
        (255, 0, 0, 150),
        (255, 255, 255)
    )

    return row


def make_data(row_count):
    rows = list()
    colors = [None, (0, 255, 255), (255, 255, 0), (255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
    words = ["Word", "War", "Why", "Jambon", "Beurre", "Pomme", "Lenalol", "Pulene"]
    processed_words = ["Apathie", "Finance", "Usul", "Gataz", "Arnault", "Ponpon"]

    for i in range(row_count):
        rows.append(Row([
            (random.choice(words), None, None),  # cell column 0
            (random.choice(words), random.choice(colors), None),  # cell column 1
            (random.choice(words), None, None),  # cell column 2
            (random.choice(words), None, random.choice(colors)),  # cell column 3
            ('...', None, None)  # cell column 4, will be computed in background
        ], {
            "random_word": random.choice(processed_words)
        }))

    return rows


if __name__ == '__main__':
    app = QApplication([])
    vue = RowTableWidget(
        auto_resize=False,
        single_row_select=True,
        context_menu_callback=None
    )

    model = RowTableModel(
        background_processing_callback=process_row
    )
    model.set_headers(['Header', 'are', 'set', 'here', 'Computed data here'])
    model.set_rows(make_data(1000))
    model.start()

    vue.set_model(model)

    vue.resize(1280, 720)
    vue.show()

    app.exec_()
