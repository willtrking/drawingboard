# coding: utf-8

__version__ = "0.1"

def create_app(config):
    import os
    from flask import Flask

    from .endpoints import init as init_endpoints
    from .db import init as init_db
    from .views import init as init_views

    _dir = os.path.dirname(os.path.realpath(__file__))
    app = Flask(
        __name__.split('.')[0],
        static_folder=_dir+"/static",
        template_folder=_dir+"/templates",
    )
    init_views(app)
    init_endpoints(app)
    init_db()

    return app