from Qt import QtWidgets
from .widgets import *
from .properties import *
from .groupbox import GroupBox


def vertical_layout(widgets, stretches=None):
    """
    Makes a QWidget with a zero-margin vertical layout, with given QWidgets and stretches

    :param widgets: A list of QWidget
    :param stretches: A list of int
    :return: A QWidget
    """
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    if stretches is None:
        stretches = [0] * len(widgets)

    for widget_, stretch in zip(widgets, stretches):
        layout.addWidget(widget_)
        layout.setStretch(layout.count() - 1, stretch)

    return widget


def make_widget(property_, parent_widget):
    if property_ is None:
        return None

    new_widget = {
        Group: _make_group,
        Label: _make_label,
        Text: _make_text,
        Enum: _make_enum,
        Integer: _make_integer,
        Bool: _make_bool,
        Filepath: _make_filepath,
        List: _make_list
    }[type(property_)](property_, parent_widget)

    return new_widget


def _make_group(property_, parent_widget):
    group = GroupBox(property_)

    parent_widget.layout().addWidget(group)
    return group


def _make_label(property_, parent_widget):
    label = LabelWidget(property_)

    parent_widget.layout().addWidget(label)
    return label


def _make_text(property_, parent_widget):
    label = QtWidgets.QLabel(property_.caption)
    lineedit = LineEdit(property_)

    parent_widget.layout().addWidget(vertical_layout(
        widgets=[label, lineedit]
    ))
    return lineedit

def _make_enum(property_, parent_widget):
    label = QtWidgets.QLabel(property_.caption)
    combo = ComboBox(property_)

    parent_widget.layout().addWidget(vertical_layout(
        widgets=[label, combo],
        stretches=[0, 100]
    ))
    return combo


def _make_integer(property_, parent_widget):
    label = QtWidgets.QLabel(property_.caption)
    spin = SpinBox(property_)

    parent_widget.layout().addWidget(vertical_layout(
        widgets=[label, spin],
        stretches=[0, 100]
    ))
    return spin


def _make_bool(property_, parent_widget):
    bool_ = CheckBox(property_)
    parent_widget.layout().addWidget(bool_)
    return bool_


def _make_filepath(property_, parent_widget):
    label = QtWidgets.QLabel(property_.caption)
    filepath = FilepathWidget(property_)
    parent_widget.layout().addWidget(vertical_layout(
        widgets=[label, filepath],
        stretches=[0, 100]
    ))
    return filepath


def _make_list(property_, parent_widget):
    label = QtWidgets.QLabel(property_.caption)
    listwidget = ListWidget(property_)
    parent_widget.layout().addWidget(vertical_layout(
        widgets=[label, listwidget],
        stretches=[0, 100]
    ))
    return listwidget
