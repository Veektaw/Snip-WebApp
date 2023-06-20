from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Url, User
from .utils import db, bcrypt, limiter, cache, login_manager
import validators
from sqlalchemy import desc
from app.helpers.view import URLCreator, generate_qr_code
from flask_caching import Cache
from flask_limiter import Limiter
from flask_jwt_extended import get_jwt_identity
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from math import ceil


snipe = Blueprint('snipe', __name__)


@snipe.route('/')
def index():
    urls = Url.query.order_by(Url.date_created.desc()).all()
    context = {
        'urls': urls,
        'new_url': request.args.get('new_url')
    }
    return render_template('home.html', **context)


@snipe.route('/create', methods=['POST'])
@limiter.limit("5 per minute")
@login_required

def create():
    
    if request.method == 'POST':
        url = request.form.get('url')

        existing_url = Url.query.filter_by(url=url, user_id=current_user.email).first()
        if existing_url:
            flash("Short Url already exists", category="error")
            return redirect(url_for('snipe.index'))

        if URLCreator.is_valid_url(url):
            url_title = URLCreator.extract_url_data(url)
            short_url = URLCreator.short_url(url)

            new_url = Url(
                url=url,
                url_title=url_title,
                short_url=short_url,
                user_id=current_user.email
            )

            try:
                new_url.save()
                flash("Success! Short URL created")
            except:
                db.session.rollback()
                return render_template('error.html')

    return redirect(url_for('snipe.index', new_url=short_url))


@snipe.route('/custom', methods=['POST'])
@limiter.limit("5 per minute")
@login_required

def custom():
    
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        custom_url = request.form.get('custom_url')
        
        existing_url = Url.query.filter_by(url=long_url, user_id=current_user.email).first()
        if existing_url:
            flash("Custom Url already exists", category="error")
            return redirect(url_for('snipe.index'))

        if URLCreator.is_valid_url(long_url):
            url_title = URLCreator.extract_url_data(long_url)
            custom_url = URLCreator.custom_url(long_url)

            new_url = Url(
                url=long_url,
                url_title=url_title,
                custom_url=custom_url,
                user_id=current_user.email
            )

            try:
                new_url.save()
                flash("Success! Short URL created")
            except:
                db.session.rollback()
                return render_template('error.html')

    return redirect(url_for('snipe.index', new_url=custom_url))



@snipe.route('/view/<int:id>/', methods=["GET", "POST"])
@login_required
def get_url_by_id(id):

    url = Url.get_by_id(id)
    return render_template('view_url.html', url=url)



# @snipe.route('/qrcode/<int:id>/', methods=["GET", "POST"])
# @login_required
# def generate_qr_code_url():
#     pass

@snipe.route('/<short_url>/<int:id>/', methods=["GET", "POST"])
def generate_qr_code_url(short_url):
    
    url = Url.query.filter_by(short_url=short_url).first()
    
    if url:
        img_io = generate_qr_code(request.host_url + url.short_url)
        return img_io.getvalue(), 200, {'Content-Type': 'image/png'}
    return 'URL not found.'



@snipe.route('/click/<string:short_url>/')
@cache.cached(timeout=50)
def redirect_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.url)
    return 'URL not found.'