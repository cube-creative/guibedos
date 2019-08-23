

def update_combo(combo, items, select=None):
    """
    Clears and updates a QComboBox with given items, and tries to restore selection without emitting a signal

    !!! note
        If the previously selected item is not found among new items, nothing is selected and a signal is emitted

    :param combo: a QComboBox
    :param items: list of strings
    :param select: a string to be set as current selection
    """
    if select is None:
        current = combo.currentText()
    else:
        current = select
    dont_emit = current in items + ['']

    combo.blockSignals(True)
    combo.clear()
    combo.addItems(items)

    if dont_emit:
        combo.setCurrentIndex(combo.findText(current))
        combo.blockSignals(False)
    else:
        combo.blockSignals(False)
        combo.setCurrentIndex(combo.findText(current))
