# coding: utf-8

from .aminations import blueprint as blueprint_aminations
from .amination_templates import blueprint as blueprint_amination_templates
from .ami_versions import blueprint as blueprint_ami_versions

from .rest import init as init_rest

def init(app):
    app.register_blueprint(blueprint_aminations)
    app.register_blueprint(blueprint_amination_templates)
    app.register_blueprint(blueprint_ami_versions)
    init_rest(app)