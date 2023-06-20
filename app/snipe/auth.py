from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Url, User
from .utils import db, bcrypt, limiter, cache, login_manager
import validators
from app.helpers.view import URLCreator
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


@auth.route("/signup", methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def signup():
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("Email already registered", category="error")
            return redirect(url_for('auth.signup'))

        password_hash = generate_password_hash(password)

        new_user = User(name=name, email=email, password=password_hash)
        new_user.save()

        flash("Account created")
        return redirect(url_for('auth.login'))

    return render_template('signup.html')



@auth.route("/login", methods=['GET', 'POST'])
def login():
    
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        flash(f'Success!! Welcome {email}')
        login_user(user)
        return redirect(url_for('snipe.index'))
    
    if user and not check_password_hash(user.password, password):
        flash("Credentials do not match", category="error")
        return redirect(url_for('auth.login'))
    
    
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

