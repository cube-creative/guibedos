import json
import jinja2
from Qt.QtCore import Qt
from Qt.QtGui import QFont
from Qt.QtWidgets import QWidget, QGridLayout, QPlainTextEdit, QLabel, QSplitter
from guibedos.helpers import WindowPosition
from .variables import Variables


EDITOR_STATE = '.csseditor'
THEME_VARIABLES = 'theme.variables'
THEME_TEMPLATE = 'theme.template'
EDITOR_STYLE = """
*{
    border-style: solid;
    background-color: white;
    color: black
}"""
COLOR_VARIANTS = [
    10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 95
]


class Editor:
    def __init__(self, app):
        self.app = app

        self.font = QFont('monospace')
        self.font.setPointSize(11)

        self.main_window = QWidget()
        self.main_window.setWindowTitle("CSS Editor")
        self.main_window.setObjectName('qssEditor')

        self.variables = Variables()
        self.variables.setObjectName('qssEditor')
        self.variables.changed.connect(self._extend_variables)
        self.variables.changed.connect(self._save_and_update)

        self.template = QPlainTextEdit()
        self.template.setObjectName('qssEditor')
        self.template.setFont(self.font)
        self.template.textChanged.connect(self._update_template)
        self.template.textChanged.connect(self._save_and_update)

        self.status = QLabel()

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.variables)
        self.splitter.addWidget(self.template)

        layout = QGridLayout(self.main_window)
        layout.addWidget(self.splitter)
        layout.addWidget(self.status)

        self.main_window.resize(800, 600)
        self.main_window.setStyleSheet(EDITOR_STYLE)

        self._variables = dict()
        self._template = None

    def _quit(self):
        with open(EDITOR_STATE, 'w+') as f_qsseditor:
            json.dump({
                'window': WindowPosition.save(self.main_window),
                'splitter': self.splitter.sizes()
            }, f_qsseditor)

    def _open(self):
        self.variables.blockSignals(True)
        self.template.blockSignals(True)

        try:
            with open(EDITOR_STATE, 'r') as f_qsseditor:
                state = json.load(f_qsseditor)
                WindowPosition.restore(self.main_window, state['window'])
                self.splitter.setSizes(state['splitter'])

            with open(THEME_VARIABLES, 'r') as f_variables:
                self.variables.variables = json.load(f_variables)

            with open(THEME_TEMPLATE, 'r') as f_template:
                self.template.setPlainText(f_template.read())
        except:
            pass

        self.variables.blockSignals(False)
        self.template.blockSignals(False)

        self._extend_variables()
        self._save_and_update()

    def exec_(self):
        self.app.aboutToQuit.connect(self._quit)
        self._open()
        self.main_window.show()
        return self.app.exec_()

    def _update_template(self):
        template = self.template.toPlainText()
        with open(THEME_TEMPLATE, 'w+') as f_template:
            f_template.write(template)

        self._template = jinja2.Template(template)

    def _extend_variables(self):
        with open(THEME_VARIABLES, 'w+') as f_variables:
            f_variables.write(json.dumps(self.variables.variables, indent=2))

        self._variables = dict()

        for variable_name, variable_value in self.variables.variables.items():
            if isinstance(variable_value, list) and len(variable_value) == 3:
                self._variables[variable_name] = 'rgb({})'.format(', '.join([str(channel) for channel in variable_value]))

                for variant in COLOR_VARIANTS:
                    channels = [str(int(channel * variant * 0.01)) for channel in variable_value]
                    self._variables[f'{variable_name}{variant:02d}'] = 'rgb({})'.format(', '.join(channels))

            else:
                self._variables[variable_name] = variable_value

        self.status.setText("Variables OK")

    def _save_and_update(self):
        self.app.setStyleSheet("")
        if self._template is None:
            return

        style = self._template.render(**self._variables)
        self.app.setStyleSheet(style)


def exec_(app):
    editor = Editor(app)
    return editor.exec_()
