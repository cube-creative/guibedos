from Qt import QtWidgets
from . import maker, handler
from guibedos.helpers import clear_layout


_ROOT_WIDGET = '_ROOT_WIDGET'



class DeclarativeForm(QtWidgets.QWidget):

    def __init__(self, root_property, parent=None, handler=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.handler = handler
        self.reload(root_property)

    def reload(self, root_property):
        if not self.layout():
            layout = QtWidgets.QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
        else:
            clear_layout(self.layout())

        self.base_widget = maker.make_widget(root_property, self)

        if self.handler:
            self.handler.assign(self.widgets())

    def widgets(self, widget=_ROOT_WIDGET):
        widgets = dict()
        if widget == _ROOT_WIDGET:
            widget = self.base_widget

        if widget is None:
            return dict()

        property_ = widget.property_

        if isinstance(widget, QtWidgets.QGroupBox):
            subdata = dict()
            for subwidget in widget.subwidgets:
                subdata.update(self.widgets(subwidget))
            widgets[property_] = subdata

        else:
            widgets[widget.property_] = widget

        return widgets

    def data(self, widget=_ROOT_WIDGET):
        data_ = dict()
        if widget == _ROOT_WIDGET:
            widget = self.base_widget

        if widget is None:
            return dict()

        property_ = widget.property_

        if isinstance(widget, QtWidgets.QGroupBox):
            subdata = dict()
            for subwidget in widget.subwidgets:
                subdata.update(self.data(subwidget))
            data_[property_.name] = subdata

        else:
            data_[widget.property_.name] = property_.value if property_.is_valid() else None

        return data_
