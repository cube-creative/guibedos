"""
CSS Theme management

CSS Themes are borrowed from FreeCAD,
more info here https://github.com/FreeCAD/FreeCAD/tree/master/src/Gui/Stylesheets
"""
import os


def _here():
    return os.path.dirname(__file__)


def parse_images(css_content):
    """
    Given a CSS content (text), replaces `qss:` with absolute path to images (i.e the `resources` folder of this repo)

    :param css_content: Text of stylesheet
    :return: Parsed text of stylesheet
    """
    css_root = os.path.join(_here(), 'resources')
    return css_content.replace('qss:', css_root.replace('\\', '/') + '/')


def set_theme(widget, theme_name):
    """
    Given a QWidget (can be a QApplication), sets the theme

    Available themes are .qss files in `resources` folder

    :param widget: a QWidget
    :param theme_name: name of the .qss file
    """
    css_root = os.path.join(_here(), 'resources')
    css_filepath = os.path.join(css_root, theme_name + '.qss')

    if not os.path.isfile(css_filepath):
        raise RuntimeError('Could not find theme file ' + css_filepath)

    with open(css_filepath, 'r') as f_css:
        style = f_css.read()

    style = parse_images(style)
    widget.setStyleSheet(style)
