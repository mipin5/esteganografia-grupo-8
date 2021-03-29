from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Sesión iniciada!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Contraseña incorrecta, inténtelo de nuevo!', category='error')
        else:
            flash('Ese nombre de usuario no existe!', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Ese nombre de usuario ya existe, escoja otro!', category='error')
        elif len(username) < 8:
            flash('El nombre de usuario debe contener al menos 8 caracteres!', category='error')
        elif password1 != password2:
            flash('Las contraseñas no coinciden!', category='error')
        elif len(password1) < 8:
            flash('La contraseña debe contener al menos 8 caracteres!', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Usuario creado!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
