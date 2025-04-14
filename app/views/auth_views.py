from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models.user_models import User
from app.forms.auth_forms import RegisterForm  # ✅ Moved here properly

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.member_page'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.member_page'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'danger')
        else:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home_page'))
