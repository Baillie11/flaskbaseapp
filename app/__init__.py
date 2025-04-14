from datetime import datetime
import os

from flask import Flask
from app.extensions import db, mail, migrate, csrf_protect, login_manager

# Initialize Flask Application
def create_app(extra_config_settings={}):
    """Create and configure the Flask application."""

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('app.settings')
    app.config.from_object('app.env_settings')
    app.config.update(extra_config_settings)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import models here AFTER db is initialized to avoid circular imports
    from app.models.user_models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .views import register_blueprints
    register_blueprints(app)

    # Setup error email logging
    init_email_error_handler(app)

    return app


def init_email_error_handler(app):
    """Configure logging to send emails for unhandled exceptions (only in production)."""
    if app.debug:
        return

    if not app.config.get('ADMINS'):
        return

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
