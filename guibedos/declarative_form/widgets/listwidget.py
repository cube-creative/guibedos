from guibedos.widgets import TagBar


class ListWidget(TagBar):

    def __init__(self, property_, parent=None):
        TagBar.__init__(self, parent)
        self.property_ = property_

        self.set_tags(self.property_.value)
        self.tags_changed.connect(self._value_changed)

    def _value_changed(self, tags):
        self.property_.value = tags
