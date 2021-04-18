import os
import json

import jinja2
from jinja2.exceptions import TemplateSyntaxError
from Qt.QtCore import Qt
from Qt.QtWidgets import QApplication, QWidget, QGridLayout, QPlainTextEdit, QSplitter, QPushButton, QLineEdit

from guibedos.helpers import WindowPosition
from .variables import Variables
from .css_text_edit import CSSTextEdit


EDITOR_STATE = '.csseditor'
THEME_VARIABLES = 'theme.variables'
THEME_TEMPLATE = 'theme.template'
COLOR_VARIANTS = [
    10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 95
]


class CSSEditor:
    """
    Make sure to instanciate *after* creating the top level widgets of your QApplication
    """
    def __init__(self, app, project_name):
        self.app = app
        self.project_name = project_name
        self._css_filepath = None

        self.main_window = QWidget()
        self.main_window.setWindowFlags(Qt.Tool)
        self.main_window.setWindowTitle("CSS Editor - " + self.project_name)

        self.variables = Variables()
        self.variables.changed.connect(self._variables_changed)
        self.variables.changed.connect(self._render_and_apply)

        self.template = CSSTextEdit()
        self.template.changed.connect(self._template_changed)
        self.template.changed.connect(self._render_and_apply)

        self.save = QPushButton('Save stylesheet to')
        self.save.clicked.connect(self._save_stylesheet)

        self.save_destination = QLineEdit()
        self.save_destination.textChanged.connect(self._destination_changed)

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.variables)
        self.splitter.addWidget(self.template)

        layout = QGridLayout(self.main_window)
        layout.addWidget(self.splitter, 0, 0, 1, 2)
        layout.addWidget(self.save, 1, 0)
        layout.addWidget(self.save_destination, 1, 1)

        self.main_window.resize(800, 600)

        self._project_dir = self._ensure_project_dir()
        self._top_level_widgets = [
            widget for widget in QApplication.topLevelWidgets() if
            widget.windowTitle() != self.main_window.windowTitle()
        ]
        self._variables = dict()
        self._template = None
        self._stylesheet = ""

        self.app.aboutToQuit.connect(self._save_editor_state)
        self._open()
        self.main_window.show()

    @property
    def css_filepath(self):
        if self._css_filepath is None:
            return self._project_dir + self.project_name + '.css'

        return self._css_filepath

    def _ensure_project_dir(self):
        dir_ = os.path.expanduser('~/CSSEditor/' + self.project_name + '/')
        if not os.path.isdir(dir_):
            os.makedirs(dir_)

        return dir_

    def _open(self):
        self.variables.blockSignals(True)
        self.template.blockSignals(True)

        try:
            with open(self._project_dir + EDITOR_STATE, 'r') as qsseditor_file:
                qsseditor = json.load(qsseditor_file)
                WindowPosition.restore(self.main_window, qsseditor['window'])
                self.splitter.setSizes(qsseditor['splitter'])
                self._css_filepath = qsseditor.get('save_destination', self.css_filepath)
                self.save_destination.setText(self._css_filepath)

            with open(self._project_dir + THEME_VARIABLES, 'r') as f_variables:
                self.variables.variables = json.load(f_variables)

            with open(self._project_dir + THEME_TEMPLATE, 'r') as f_template:
                self.template.set_plain_text(f_template.read())
        except Exception as e:
            pass
        self.variables.blockSignals(False)
        self.template.blockSignals(False)

        self._template_changed()
        self._variables_changed()
        self._render_and_apply()

    def _destination_changed(self):
        self._css_filepath = self.save_destination.text()
        self._save_editor_state()

    def _save_editor_state(self):
        with open(self._project_dir + EDITOR_STATE, 'w+') as f_qsseditor:
            json.dump({
                'window': WindowPosition.save(self.main_window),
                'splitter': self.splitter.sizes(),
                'save_destination': self.css_filepath
            }, f_qsseditor)

    def _template_changed(self):
        template = self.template.plain_text()
        with open(self._project_dir + THEME_TEMPLATE, 'w+') as f_template:
            f_template.write(template)

        try:
            self._template = jinja2.Template(template)
        except TemplateSyntaxError:
            pass

    def _variables_changed(self):
        with open(self._project_dir + THEME_VARIABLES, 'w+') as f_variables:
            f_variables.write(json.dumps(self.variables.variables, indent=2))

        self._variables = dict()

        for variable_name, variable_value in self.variables.variables.items():
            if isinstance(variable_value, list) and len(variable_value) == 3:
                self._variables[variable_name] = 'rgb({})'.format(', '.join([str(channel) for channel in variable_value]))

                for variant in COLOR_VARIANTS:
                    channels = [str(int(channel * variant * 0.01)) for channel in variable_value]
                    self._variables['{}{:02d}'.format(variable_name, variant)] = 'rgb({})'.format(', '.join(channels))

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
        stylesheet = [
            "/* GUI Bedos - CSS Template */",
            "/****************************/",
            "",
            "/* VARIABLES",
            json.dumps(self.variables.variables, indent=2),
            "/****************************/",
            "",
            "/* TEMPLATE",
            self.template.plain_text().replace('*/', '*|'),
            "/****************************/",
            "",
            "/* ACTUAL CSS */",
            "",
            self._stylesheet
        ]
        with open(self.css_filepath, 'w+') as f_stylesheet:
            f_stylesheet.write('\n'.join(stylesheet))
