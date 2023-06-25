from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Url, User
from .utils import db, bcrypt, limiter, cache, login_manager
from app.helpers.view import URLCreator
from flask_caching import Cache
from flask_limiter import Limiter
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


from werkzeug.security import generate_password_hash, check_password_hash

@auth.route("/signup", methods=['GET', 'POST'])
@limiter.limit("2 per minute")
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
      
        if password != password_confirmation:
            flash("Password confirmation does not match", category="error")
            return redirect(url_for('auth.signup'))
     
        if len(password) < 8 or not any(c in "!@#$%^&*(),.?\":{}|<>1234567890" for c in password):
            flash("Password must be at least 8 characters long and contain a special character or number", category="error")
            return redirect(url_for('auth.signup'))

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("Email already registered", category="error")
            return redirect(url_for('auth.signup'))

        phone_number_exists = User.query.filter_by(phone_number=phone_number).first()
        if phone_number_exists:
            flash("Phone number already registered", category="error")
            return redirect(url_for('auth.signup'))
        
        password_hash = generate_password_hash(password)

        new_user = User(name = name,
                        phone_number = phone_number,
                        email = email, 
                        password = password_hash)
        flash("Account created")
        new_user.save()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')




@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User does not exist", category="error")
            
        elif check_password_hash(user.password, password):
            flash(f'Success!! Welcome {email}')
            login_user(user)
            return redirect(url_for('snipe.home'))
        
        else:
            flash("Credentials do not match", category="error")

    return render_template('signin.html')


    
    

@auth.route('/protected')
@login_required
def protected():
    
    return render_template('protected.html', email=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    
    flash('Goodbye')
    logout_user()

    return redirect(url_for('snipe.index'))



@auth.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password, current_password):
            flash("Incorrect current password", category="error")
            return redirect(url_for('auth.change_password'))

        if new_password != confirm_password:
            flash("Password confirmation does not match", category="error")
            return redirect(url_for('auth.change_password'))

        if len(new_password) < 8 or not any(c in "!@#$%^&*(),.?\":{}|<>1234567890" for c in new_password):
            flash("New password must be at least 8 characters long and contain a special character or number", category="error")
            return redirect(url_for('auth.change_password'))

        if check_password_hash(current_user.password, new_password):
            flash("New password must be different from the current password", category="error")
            return redirect(url_for('auth.change_password'))

        current_user.password = generate_password_hash(new_password)
        current_user.save()

        flash("Password changed successfully")
        return redirect(url_for('auth.profile'))

    return render_template('password_change.html')







@auth.route('/<int:user_id>/profile/', methods=["GET", "POST"])
@login_required
def profile(user_id):

    user = User.query.filter_by(id=current_user.id).first()
    
    page = request.args.get('page', 1, type=int)
    per_page = 5 

    urls = Url.query.filter_by(user_id=current_user.email).order_by(desc(Url.date_created)).paginate(page=page, per_page=per_page)
    
    context = {
    'user': user.name,
    'email': user.email,
    'phone_number': user.phone_number,
    'date': user.created_at,
    'urls': urls,
    'new_url': request.args.get('new_url'),
    'custom_url_created': request.args.get('custom_url_created'),
    }

    
    return render_template('profile.html', **context)