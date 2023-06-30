import os
from datetime import timedelta

# base_dir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'snipe.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
STORAGE_URI = os.environ.get('MEMCACHED_URI', '')
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

