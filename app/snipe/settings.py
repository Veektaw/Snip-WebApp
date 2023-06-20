import os

base_dir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'snipe.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = '9e6e82e501e740149e01727700939803'
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
