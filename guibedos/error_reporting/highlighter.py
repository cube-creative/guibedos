import re
from Qt.QtCore import Qt
from Qt.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont


LINE_FILE_RE = re.compile(r"^\s\s\S.+")
LINE_FILE_FORMAT = QTextCharFormat()
LINE_FILE_FORMAT.setForeground(Qt.lightGray)

LINE_CODE_RE = re.compile(r"^\s\s\s\s\S.+")
LINE_CODE_FORMAT = QTextCharFormat()
LINE_CODE_FORMAT.setFontWeight(QFont.Bold)

FILE_RE = re.compile(r"\"[^\"]+\"")
FILE_FORMAT = QTextCharFormat()
FILE_FORMAT.setFontItalic(True)
FILE_FORMAT.setForeground(Qt.black)

CALL_RE = re.compile(r", in ([^$]+)$")
CALL_FORMAT = QTextCharFormat()
CALL_FORMAT.setFontWeight(QFont.Bold)
CALL_FORMAT.setForeground(Qt.magenta)

LINE_RE = re.compile(r"line \d+")
LINE_FORMAT = QTextCharFormat()
LINE_FORMAT.setForeground(Qt.green)


class TracebackHighlighter(QSyntaxHighlighter):
    RULES = {
        LINE_FILE_RE: LINE_FILE_FORMAT,
        LINE_CODE_RE: LINE_CODE_FORMAT,
        CALL_RE: CALL_FORMAT,
        LINE_RE: LINE_FORMAT
    }

    def __init__(self, parent=None):
        QSyntaxHighlighter.__init__(self, parent)

    def highlightBlock(self, text):
        for expression, style in self.RULES.items():

            for found in expression.finditer(text):
                start, end = found.span()
                self.setFormat(start, end - start, style)
