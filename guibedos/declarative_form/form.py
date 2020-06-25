from Qt import QtWidgets
from . import maker, handler


_ROOT_WIDGET = '_ROOT_WIDGET'


def _clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                _clear_layout(item.layout())


class DeclarativeForm(QtWidgets.QWidget):

    def __init__(self, root_property, parent=None, handler=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.handler = handler
        self.reload(root_property)

    def _assign_subdata(self, data_, property, subdata, get_property_widget):
        if get_property_widget:
            data_[property] = subdata
        else:
            data_[property.name] = subdata
        return data

    def _assign_value(self, data_, property, widget, get_property_widget):
        if get_property_widget:
            data_[widget.property_] = widget
        else:
            data_[widget.property_.name] = property.value if property.is_valid() else None
        return data

    def _retrieve_data(self, widget, get_property_widget):
        data_ = dict()
        if widget == _ROOT_WIDGET:
            widget = self.base_widget

        if widget is None:
            return dict()

        property_ = widget.property_

        if isinstance(widget, QtWidgets.QGroupBox):
            subdata = dict()
            for subwidget in widget.subwidgets:
                subdata.update(self._retrieve_data(subwidget, get_property_widget))

            _assign_subdata(data_, property_, subdata, get_property_widget)

        else:
            _assign_value(data_, property_, widget, get_property_widget)

        return data_

    def reload(self, root_property):
        if not self.layout():
            layout = QtWidgets.QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
        else:
            _clear_layout(self.layout())

        self.base_widget = maker.make_widget(root_property, self)

        if self.handler:
            self.handler.assign(self.widgets())

    def widgets(self, widget=_ROOT_WIDGET):
        return self._retrieve_data(widget, get_property_widget=True)

    def data(self, widget=_ROOT_WIDGET):
        return self._retrieve_data(widget, get_property_widget=False)
