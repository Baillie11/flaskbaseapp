from datetime import datetime
import os

from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_user import UserManager
from flask_wtf.csrf import CSRFProtect


# Instantiate Flask extensions
csrf_protect = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

# Initialize Flask Application
def create_app(extra_config_settings={}):
    """Create and configure the Flask application."""

    # Instantiate Flask
    app = Flask(__name__)

    # Load base and environment-specific settings
    app.config.from_object('app.settings')        # Load default/base config
    app.config.from_object('app.env_settings')    # Load local overrides (email, DB, etc.)
    app.config.update(extra_config_settings)      # Any extras passed in programmatically

    # Setup all Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf_protect.init_app(app)

    # Register app blueprints (routes/views)
    from .views import register_blueprints
    register_blueprints(app)

    # Add support for detecting hidden form fields in templates
    from wtforms.fields import HiddenField
    app.jinja_env.globals['bootstrap_is_hidden_field'] = lambda field: isinstance(field, HiddenField)

    # Setup Flask-User for account management
    from .models.user_models import User
    user_manager = UserManager(app, db, User)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    # Setup error email logging (only if app.config.ADMINS is set)
    init_email_error_handler(app)

    return app


def init_email_error_handler(app):
    """Configure logging to send emails for unhandled exceptions (only in production)."""
    if app.debug:
        return  # Don’t send emails during development

    if not app.config.get('ADMINS'):
        return  # No admins defined to send to

    try:
        import logging
        from logging.handlers import SMTPHandler

        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_DEFAULT_SENDER'],
            toaddrs=app.config['ADMINS'],
            subject=app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error'),
            credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
            secure=() if app.config.get('MAIL_USE_TLS') else None,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    except Exception as e:
        app.logger.warning(f"Email error logger setup failed: {e}")
