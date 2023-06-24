from flask import Flask
from .views import cache, limiter
from .utils import db, bcrypt, login_manager, migrate, cache, limiter
from .models import User, Url, Country
from flask_limiter import Limiter
from flask_caching import Cache
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_cors import CORS
from .auth import auth
from .views import snipe




login_manager.login_view = 'snipe.login'

load_dotenv()

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    CORS(app)

    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(snipe)
    app.register_blueprint(auth)
    
    limiter = Limiter(key_func=get_remote_address, app=app,
        storage_uri="memcached://localhost:5000",
        storage_options={}
        )
    
    cache.init_app(app, config={'CACHE_TYPE': 'simple'}) 
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'url': Url,
            'user': User,
            'country': Country
        }

    return app