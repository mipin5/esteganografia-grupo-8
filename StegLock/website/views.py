from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Medium
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        medium = request.form.get('medium')
        message = request.form.get('message')
        password = request.form.get('password')
        medium_name = medium[:-4]
        medium_type = medium[-3:]
        if len(message) < 1:
            flash('El mensaje es muy corto', category='error')
        else:
            new_medium = Medium(name=medium_name, mtype=medium_type, password=password, user_id=current_user.id)
            db.session.add(new_medium)
            db.session.commit()
            flash('Medio encriptado!', category='success')

    return render_template("encrypt.html", user=current_user)

@views.route('/activity', methods=['GET'])
def activity():
    return render_template("activity.html", user=current_user)