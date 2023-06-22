from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from .models import Url, Country
from .utils import db, bcrypt, limiter, cache, login_manager
from sqlalchemy import desc
from app.helpers.view import URLCreator, generate_qr_code
from flask_caching import Cache
from flask_limiter import Limiter
from flask_jwt_extended import get_jwt_identity
from flask_limiter.util import get_remote_address
from flask_login import login_required, current_user
import qrcode
from io import BytesIO
import io
import os


snipe = Blueprint('snipe', __name__)


@snipe.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5 

    urls = Url.query.filter_by(user_id=current_user.email).order_by(desc(Url.date_created)).paginate(page=page, per_page=per_page)
    context = {
        'urls': urls,
        'new_url': request.args.get('new_url'),
        'custom_url_created': request.args.get('custom_url_created'),
    }
    return render_template('home.html', **context)


@snipe.route('/create', methods=['POST', 'GET'])
@limiter.limit("5 per minute")
@login_required
def create():
    if request.method == 'POST':
        url = request.form.get('url')

        existing_url = Url.query.filter_by(url=url, user_id=current_user.email).first()
        if existing_url:
            flash("Short URL already exists", category="error")
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

    return render_template('create.html')



@snipe.route('/custom', methods=['POST', 'GET'])
@limiter.limit("5 per minute")
@login_required
def custom():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        custom_url_entry = request.form.get('custom_url_entry')

        existing_url = Url.query.filter_by(url=long_url, user_id=current_user.email).first()
        if existing_url:
            flash("Custom URL already exists", category="error")
            return redirect(url_for('snipe.index'))

        if URLCreator.is_valid_url(long_url):
            url_title = URLCreator.extract_url_data(long_url)
            custom_url = URLCreator.custom_url(long_url, custom_url_entry)

            custom_url_created = Url(
                url=long_url,
                url_title=url_title,
                custom_url=custom_url,
                user_id=current_user.email
            )

            try:
                custom_url_created.save()
                flash("Success! Custom URL created")
            except:
                db.session.rollback()
                return render_template('error.html')

    return redirect(url_for('snipe.index', custom_url_created=custom_url))




@snipe.route('/view/<int:id>/', methods=["GET", "POST"])
@login_required
def get_url_by_id(id):

    url = Url.get_by_id(id)
    return render_template('view_url.html', url=url)



@snipe.route('/delete/<int:id>/', methods=['POST', 'GET', 'DELETE'])
@login_required
def delete_url(id):
    
    url = Url.get_by_id(id)
    if url:
        db.session.delete(url)
        db.session.commit()
        flash("URL deleted successfully")
        
    return redirect(url_for('snipe.index'))



@snipe.route('/qrcode/<int:id>/', methods=['POST', 'GET'])
def generate_qr_code_url(id):
    url = Url.get_by_id(id)
    
    if url:
        
        img = qrcode.make(url.url)
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        qr_code_data = img_io.getvalue() 
        
        url.qr_code_url = qr_code_data
        url.save()
        
        return send_file(img_io, mimetype='image/png')
    
    return 'URL not found.', 404



@snipe.route('/click/<int:id>/', methods=['POST', 'GET'])
@cache.cached(timeout=50)
def redirect_url(id):
    url = Url.query.get(id)
    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.url)
    return 'URL not found.'


@snipe.route('/country', methods=['POST', 'GET'])
def save_country():
    country_code = request.form.get('country_code')
    click = Country(country_code=country_code)
    click.save()

    return 'Country saved successfully'