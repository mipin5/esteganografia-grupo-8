from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Medium, Img
from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        medium = request.files['medium']
        message = request.form.get('message')
        password = request.form.get('password')
        if len(message) < 1:
            flash('El mensaje es muy corto', category='error')
        else:
            medium_name = secure_filename(medium.filename)
            medium_type = medium.medium_type
            medium_password = generate_password_hash(password, method='sha256')
            if medium_type != 'png'
                converted_img = Image.open(medium).convert('RGB')
                converted_img.save(f'{medium_name}.png', 'png')
            medium_file = converted_img.read()
            new_medium = Medium(name=medium_name, mtype=medium_type, password=medium_password, user_id=current_user.id)
            db.session.add(new_medium)
            db.session.commit()
            encoded_image = encodeStringInImage(message, medium_file, medium_password)
            flash('Medio encriptado!', category='success')

    return render_template("encrypt.html", user=current_user)

@views.route('/activity', methods=['GET'])
def activity():
    return render_template("activity.html", user=current_user)
