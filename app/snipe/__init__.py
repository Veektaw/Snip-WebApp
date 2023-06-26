from flask import Flask, session
from .views import cache, limiter
from .utils import db, bcrypt, login_manager, migrate, cache, limiter, mail, admin
from .models import User, Url, Country
from flask_limiter import Limiter
from flask_caching import Cache
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_cors import CORS
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .auth import auth
from .views import snipe
from datetime import timedelta





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
    mail = Mail(app)

    app.register_blueprint(snipe)
    app.register_blueprint(auth)
    
    
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session)) 
    admin.add_view(ModelView(Url, db.session)) 
    admin.add_view(ModelView(Country, db.session))
    
    
    limiter = Limiter(key_func=get_remote_address, app=app,
                  storage_uri="memcached://localhost:11211",
                  storage_options={})

    
    cache.init_app(app, config={'CACHE_TYPE': 'simple'}) 
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'url': Url,
            'user': User,
            'country': Country
        }
        
    @app.before_request
    def refresh_session():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=7)

    return app