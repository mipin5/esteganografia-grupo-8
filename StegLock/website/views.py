from flask import Blueprint, render_template, request, flash, jsonify, send_file
from flask_login import login_required, current_user
from .models import Medium
from . import db
from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import json, os
from io import BytesIO
from .stegimage import encodeStringInImage, encodeFileInImage, decodeImage

views = Blueprint('views', __name__)

#Crea la carpeta temp dentro del directorio principal del proyecto si no existe
def createFolder():
    created_upload_path = 'temp/'
    try:
        if not os.path.exists(created_upload_path):
            os.makedirs(created_upload_path)
    except OSError:
        print ('Error creando directorio' + created_upload_path)

def deleteTempFiles():
    directory = 'temp/'
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))

@views.route('/', methods=['GET'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    try:  
        if request.method == 'POST':
            deleteTempFiles()
            medium = request.files['medium']
            message = request.form.get('message')
            textfile = request.files['textfile']
            password = request.form.get('password')
            if not medium:
                flash('No se encontró ningún medio', category='error')
            elif not textfile and len(message) < 1:
                flash('No se ha encontrado elemento a encriptar', category='error')
            elif textfile and len(message) > 0:
                flash('No se puede ingresar más de un elemento a encriptar', category='error')
            else:
                medium_name = secure_filename(medium.filename)
                medium_type = medium.mimetype
                medium_password = generate_password_hash(password, method='sha256')

                #Convierte imagen a png
                ima = Image.open(medium)
                f = BytesIO()
                ima.save(f, format='PNG')
                f.seek(0)
                medium_file = Image.open(f)

                #Registra en base de datos
                new_medium = Medium(name=medium_name, mtype=medium_type, password=medium_password, user_id=current_user.id)
                db.session.add(new_medium)
                db.session.commit()

                #Codifica de acuerdo a si se ingresó una cadena o un archivo de texto
                createFolder()
                if len(message) > 0:
                    encoded_image = encodeStringInImage(message, medium_file, password)
                else:
                    textfile.save(f'temp/textfile.txt')
                    encoded_image = encodeFileInImage('textfile.txt', medium_file, password)

                #Guarda la imagen resultado en archivo temporal
                encoded_image.seek(0)
                encoded_image.save(f'temp/encoded.png')

                #Crea la respuesta del servidor como descarga de la imagen y elimina la imagen temporal
                upload_path = f'../temp/encoded.png' #send_file() lee desde la ubicación del archivo views.py
                flash('Medio encriptado!', category='success')
                return send_file(upload_path, as_attachment=True)
                #os.remove(f'../temp/encoded.png')

        return render_template("encrypt.html", user=current_user)
    
    except:
        flash("Error del sistema", category='error')
        return render_template("encrypt.html", user=current_user)


@views.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    try:
        decoded_result = ''
        if request.method == 'POST':
            deleteTempFiles()
            medium = request.files['medium']
            password = request.form.get('password')
            if not medium:
                flash('No se encontró ningún medio', category='error')
            else:
                #Convierte imagen a png
                ima = Image.open(medium)
                f = BytesIO()
                ima.save(f, format='PNG')
                f.seek(0)
                medium_file = Image.open(f)

                decoded_result = decodeImage(medium_file, password)
                download_path = f'../temp/decodedmessage.txt'

                if decoded_result == 'temp/decodedmessage.txt':
                    flash('Medio desencriptado!', category='success')
                    return send_file(download_path, as_attachment=True)
                elif decoded_result == '0':
                    flash('Contraseña incorrecta!', category='error')
                    return render_template("decrypt.html", user=current_user)
                else:
                    flash('Medio descifrado!', category='success')
                    return render_template("decrypt.html", user=current_user, decoded_message=decoded_result)
        
        return render_template("decrypt.html", user=current_user)

    except:
        flash("Error del sistema", category='error')
        return render_template("decrypt.html", user=current_user, data=decoded_result)


@views.route('/activity', methods=['GET'])
def activity():
    return render_template("activity.html", user=current_user)