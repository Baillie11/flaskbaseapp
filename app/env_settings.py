# app/env_settings.py

# Flask general settings
DEBUG = True
SECRET_KEY = 'super-secret-key-change-this'  # Replace with a secure key in production

# SQLAlchemy database config (persistent SQLite file)
SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskbaseapp.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids warning

# Flask-Mail config for Gmail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'andrewgbaillie@gmail.com'
MAIL_PASSWORD = 'jays irrq ywoy zxys'  # ⚠️ App password, never use regular Gmail password
MAIL_DEFAULT_SENDER = 'andrewgbaillie@gmail.com'

# Flask-User config
USER_ENABLE_CONFIRM_EMAIL = False
USER_EMAIL_SENDER_EMAIL = 'andrewgbaillie@gmail.com'
USER_EMAIL_SENDER_NAME = 'FLASKBASEAPP Support'

# Stripe API config - Test mode
STRIPE_PUBLIC_KEY = 'pk_test_vGxjfUaSwMLWBEQobMzCltFd'
STRIPE_SECRET_KEY = 'sk_test_CV9YXEGE6ZMP2CLr7nppHejp'
