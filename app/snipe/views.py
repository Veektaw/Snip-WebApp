from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify, abort
from .models import Url, Country, User
from .utils import db, bcrypt, limiter, cache, login_manager
from sqlalchemy import desc
from app.helpers.view import URLCreator, generate_qr_code
from flask_caching import Cache
from flask_jwt_extended import get_jwt_identity
from flask_limiter.util import get_remote_address
from flask_login import login_required, current_user
import qrcode
import io
import base64


snipe = Blueprint('snipe', __name__)



@snipe.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('snipe.home'))
    else:
        return render_template('frontIndex.html')


@snipe.route('/home')
@login_required
def home():
    
    page = request.args.get('page', 1, type=int)
    per_page = 5 

    urls = Url.query.filter_by(user_id=current_user.email).order_by(desc(Url.date_created)).paginate(page=page, per_page=per_page)
    new_url = request.args.get('new_url')
    custom_url_created = request.args.get('custom_url_created')
    context = {
        'urls': urls,
        'new_url': new_url,
        'custom_url_created': custom_url_created
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
            return redirect(url_for('snipe.home'))

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
            

        return redirect(url_for('snipe.home', new_url=short_url))
        



@snipe.route('/<random_string_combination>')
def redirect_to_original(random_string_combination):
    short_url = f"http://{request.host}/{random_string_combination}"
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        url.clicks += 1
        url.save()
        return redirect(url.url)
    else:
        abort(404)



@snipe.route('/custom', methods=['POST', 'GET'])
@limiter.limit("5 per minute")
@login_required
def custom():
    if request.method == 'POST':
        url = request.form.get('url')
        custom_url_entry = request.form.get('custom_url_entry')
        custom_url = None  # Assign a default value to custom_url

        existing_url = Url.query.filter_by(custom_url=custom_url_entry, user_id=current_user.email).first()
        if existing_url:
            flash("Custom URL already exists", category="error")
            return redirect(url_for('snipe.home'))

        if URLCreator.is_valid_url(url):
            url_title = URLCreator.extract_url_data(url)
            custom_url = f"http://{request.host}/{custom_url_entry}"

            custom_url_created = Url(
                url=url,
                url_title=url_title,
                short_url=custom_url,
                user_id=current_user.email
            )

            try:
                custom_url_created.save()
                flash("Success! Custom URL created")
            except:
                db.session.rollback()
                return render_template('error.html')

        return redirect(url_for('snipe.home', custom_url_created=custom_url))




@snipe.route('/<int:id>/view/', methods=["GET", "POST"])
@limiter.limit("5 per minute")
@cache.cached(timeout=30)
@login_required
def view(id):

    url = Url.get_by_id(id)
    return render_template('view.html', url=url)



@snipe.route('/<int:id>/delete', methods=['POST', 'GET', 'DELETE'])
@limiter.limit("5 per minute")
@cache.cached(timeout=30)
@login_required
def delete_url(id):
    
    url = Url.get_by_id(id)
    if url:
        db.session.delete(url)
        db.session.commit()
        flash("URL successfully deleted")
        
    return redirect(url_for('auth.profile', user_id=current_user.id))
    



@snipe.route('/<int:id>/qrcode/', methods=['POST', 'GET'])
@login_required
@limiter.limit("5 per minute")
def generate_qr_code_url(id):
    url = Url.get_by_id(id)
    
    if url:
        img = qrcode.make(url.url)
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        qr_code_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        url.qr_code_url = qr_code_data
        url.save()
        
        return send_file(img_io, mimetype='image/png')
    
    return 'URL not found.', 404



@snipe.route('/save_country', methods=['POST'])
@login_required
def save_country():
    url_id = request.form.get('url_id')
    country_name = request.form.get('country_name')
    clicks = request.form.get('clicks')

    url = Url.get_by_id(url_id)
    if url:
        country = Country(country=country_name, clicks=clicks, url_id=url_id)
        country.save()
        return jsonify({'message': 'Country saved successfully.'})
    else:
        return jsonify({'error': 'URL not found.'}), 404



@snipe.route('/about', methods=['GET'])
@login_required
@limiter.limit("5 per minute")
@cache.cached(timeout=59)
def about():
    
    return render_template('about.html')


@snipe.route('/<int:user_id>/edit/', methods=['PATCH', 'PUT', 'GET', 'POST'])
@login_required
@limiter.limit("1 per week")
def edit(user_id):
    
    profile = User.query.filter_by(email=current_user.email).first()

    if request.method == 'POST':
        profile.name = request.form['name']
        profile.email = request.form['email']
        profile.phone_number = request.form['phone_number']
    
        db.session.commit()
        flash("Success! Profile updated")
        return redirect(url_for('auth.profile', user_id=current_user.id))
    
    return render_template('edit.html')
