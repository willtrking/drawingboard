# coding: utf-8

from drawingboard.lib.amination_templates import cli_to_str

def init(app):
    app.jinja_options['extensions'].append('jinja2.ext.do')
    app.jinja_env.filters['format_cli_args'] = cli_to_str