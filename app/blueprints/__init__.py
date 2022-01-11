from .home import blueprint as home
from .dashboard import blueprint as dashboard


def register_blueprints(app):
    app.register_blueprint(home)
    app.register_blueprint(dashboard, url_prefix='/dashboard')
