import os
import json
import jinja2
from Qt.QtCore import Qt
from Qt.QtGui import QFont
from Qt.QtWidgets import QApplication, QWidget, QGridLayout, QPlainTextEdit, QSplitter, QPushButton
from guibedos.helpers import WindowPosition
from .variables import Variables


EDITOR_STATE = '.csseditor'
THEME_VARIABLES = 'theme.variables'
THEME_TEMPLATE = 'theme.template'
COLOR_VARIANTS = [
    10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 95
]


class CSSEditor:
    def __init__(self, app, project_name):
        self.app = app
        self.project_name = project_name

        self.font = QFont('monospace')

        self.main_window = QWidget()
        self.main_window.setWindowFlags(Qt.Tool)
        self.main_window.setWindowTitle("CSS Editor - " + self.project_name)

        self.variables = Variables()
        self.variables.changed.connect(self._variables_changed)
        self.variables.changed.connect(self._render_and_apply)

        self.template = QPlainTextEdit()
        self.template.setFont(self.font)
        self.template.textChanged.connect(self._template_changed)
        self.template.textChanged.connect(self._render_and_apply)

        self.save = QPushButton('Save stylesheet')
        self.save.clicked.connect(self._save_stylesheet)

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.variables)
        self.splitter.addWidget(self.template)

        layout = QGridLayout(self.main_window)
        layout.addWidget(self.splitter)
        layout.addWidget(self.save)

        self.main_window.resize(800, 600)

        self._project_dir = self._ensure_project_dir()
        self._top_level_widgets = list()
        self._variables = dict()
        self._template = None
        self._stylesheet = ""

    def _ensure_project_dir(self):
        dir_ = os.path.expanduser('~/CSSEditor/' + self.project_name + '/')
        if not os.path.isdir(dir_):
            os.makedirs(dir_)

        return dir_

    def _open(self):
        self.variables.blockSignals(True)
        self.template.blockSignals(True)

        try:
            with open(self._project_dir + EDITOR_STATE, 'r') as f_qsseditor:
                state = json.load(f_qsseditor)
                WindowPosition.restore(self.main_window, state['window'])
                self.splitter.setSizes(state['splitter'])

            with open(self._project_dir + THEME_VARIABLES, 'r') as f_variables:
                self.variables.variables = json.load(f_variables)

            with open(self._project_dir + THEME_TEMPLATE, 'r') as f_template:
                self.template.setPlainText(f_template.read())
        except:
            pass

        self.variables.blockSignals(False)
        self.template.blockSignals(False)

        self._template_changed()
        self._variables_changed()
        self._render_and_apply()

    def _quit(self):
        with open(self._project_dir + EDITOR_STATE, 'w+') as f_qsseditor:
            json.dump({
                'window': WindowPosition.save(self.main_window),
                'splitter': self.splitter.sizes()
            }, f_qsseditor)

    def _template_changed(self):
        template = self.template.toPlainText()
        with open(self._project_dir + THEME_TEMPLATE, 'w+') as f_template:
            f_template.write(template)

        self._template = jinja2.Template(template)

    def _variables_changed(self):
        with open(self._project_dir + THEME_VARIABLES, 'w+') as f_variables:
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

    def _apply_style(self, style):
        for widget in self._top_level_widgets:
            widget.setStyleSheet(style)

    def _render_and_apply(self):
        self._apply_style("")

        if self._template is None:
            return

        self._stylesheet = self._template.render(**self._variables)
        self._apply_style(self._stylesheet)

    def _save_stylesheet(self):
        with open(self._project_dir + self.project_name + '.css', 'w+') as f_stylesheet:
            f_stylesheet.write(self._stylesheet)

    def exec_(self):
        self._top_level_widgets = [
            widget for widget in QApplication.topLevelWidgets() if widget.windowTitle() != self.main_window.windowTitle()
        ]
        self.app.aboutToQuit.connect(self._quit)
        self._open()
        self.main_window.show()

        return self.app.exec_()
