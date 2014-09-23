# coding: utf-8

from .amination_templates import blueprint as blueprint_amination_templates
from .ami_versions import blueprint as blueprint_ami_versions
from .aminations import blueprint as blueprint_aminations

def init(app):
    app.register_blueprint(blueprint_amination_templates)
    app.register_blueprint(blueprint_ami_versions)
    app.register_blueprint(blueprint_aminations)