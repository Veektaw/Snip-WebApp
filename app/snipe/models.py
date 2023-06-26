from datetime import datetime
from .utils import db, login_manager, bcrypt, admin
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.Text(), unique=True)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    url = db.relationship('Url', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"
    
    @classmethod
    def get_by_id(cls, id):
        url = db.session.get(Url, id)
        return url

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
        
    



class Url(db.Model):
    
    __tablename__  = 'urls'
    
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(512))
    short_url = db.Column(db.String(5), unique=True)
    custom_url = db.Column(db.String(50), unique=False)
    qr_code_url = db.Column(db.String(300), nullable=True, unique=False)
    url_title = db.Column(db.String(900), nullable=True, unique=False)
    clicks = db.Column(db.Integer(), default=0)
    date_created = db.Column(db.DateTime(), default=datetime.now)
    country_origin = db.relationship('Country', backref='countries', lazy=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<url {self.id}>"
    

    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
    @classmethod
    def get_by_id(cls, id):
        url = db.session.get(Url, id)
        return url

    @classmethod
    def total_clicks(cls, id):
        urls = Url.query.filter_by(creator = id).all()
        total_url_clicks = sum([url.visited for url in urls])
        return total_url_clicks 
    
    @classmethod
    def total_urls(cls, id):
        return Url.query.filter_by(creator = id).count() 

    @classmethod
    def check_url(cls , url):
        url_exists = cls.query.filter_by(short_url = url).first()
        return True if url_exists else False
    

    
    
class Country(db.Model):
    
    __tablename__  = 'countries'
    
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    clicks = db.Column(db.Integer(), default=0)
    url_id = db.Column(db.String(), db.ForeignKey('urls.id'))
    
    def __repr__(self):
        return f"<url {self.id}>"
    

    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
    @classmethod
    def get_by_id(cls, id):
        url = db.session.get(Url, id)
        return url