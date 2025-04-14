from .main_views import main_blueprint
from .auth_views import auth_blueprint

def register_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
