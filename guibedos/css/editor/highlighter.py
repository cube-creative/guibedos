import re
from Qt.QtCore import Qt
from Qt.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont


COMMENT_RE = re.compile(r"/\*.+\*/")
COMMENT_FORMAT = QTextCharFormat()
COMMENT_FORMAT.setFontItalic(True)
COMMENT_FORMAT.setForeground(Qt.darkGray)

JINJA_RE = re.compile(r"{{.+}}")
JINJA_FORMAT = QTextCharFormat()
JINJA_FORMAT.setFontWeight(QFont.Bold)
JINJA_FORMAT.setForeground(Qt.darkMagenta)

QCLASS_RE = re.compile(r"Q[\w]+")
QCLASS_FORMAT = QTextCharFormat()
QCLASS_FORMAT.setFontWeight(QFont.Bold)
QCLASS_FORMAT.setForeground(Qt.darkGreen)

QSUBELEMENT_RE = re.compile(r"::([\w-]+)")
QSUBELEMENT_FORMAT = QTextCharFormat()
QSUBELEMENT_FORMAT.setFontWeight(QFont.Bold)
QSUBELEMENT_FORMAT.setForeground(Qt.darkBlue)

PROPERTY_RE = re.compile(r"\[[^=]+=[^\]]+]")
PROPERTY_FORMAT = QTextCharFormat()
PROPERTY_FORMAT.setFontItalic(True)
PROPERTY_FORMAT.setForeground(Qt.darkGreen)


class TemplateHighlighter(QSyntaxHighlighter):
    RULES = {
        QCLASS_RE: QCLASS_FORMAT,
        QSUBELEMENT_RE: QSUBELEMENT_FORMAT,
        PROPERTY_RE: PROPERTY_FORMAT,
        JINJA_RE: JINJA_FORMAT,
        COMMENT_RE: COMMENT_FORMAT,
    }

    def __init__(self, parent=None):
        QSyntaxHighlighter.__init__(self, parent)

    def highlightBlock(self, text):
        for expression, style in self.RULES.items():

            for found in expression.finditer(text):
                start, end = found.span()
                self.setFormat(start, end - start, style)
