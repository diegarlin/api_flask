# routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .extensions import bcrypt
from .models import User, db
import re
from flask_mail import Message
from .extensions import mail
import requests
import logging

main = Blueprint('main', __name__)

@main.route('/hola', methods=['GET'])
def hola():
    return jsonify({"msg": "hola"}), 200

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username').strip()
    password = data.get('password').strip()
    email = data.get('email').strip()
    deviceID = data.get('deviceID')

    # Verificar si hay espacios en blanco en el username
    if ' ' in username:
        return jsonify({"msg": "El nombre de usuario no puede contener espacios en blanco"}), 400

    # Verificar si hay espacios en blanco en el password
    if ' ' in password:
        return jsonify({"msg": "La contraseña no puede contener espacios en blanco"}), 400

    # Verificar si el usuario ya existe
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "El nombre de usuario ya está en uso"}), 400
    
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"msg": "El correo ya está en uso"}), 400

    # Verificar si el deviceID ya está en uso
    existing_device = User.query.filter_by(deviceID=deviceID).first()
    if existing_device:
        return jsonify({"msg": "El deviceID ya está en uso"}), 400

    # Verificar si la contraseña cumple con los requisitos
    if not (len(password) >= 6 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)):
        return jsonify({"msg": "La contraseña debe tener al menos 6 caracteres, una mayúscula, una minúscula y un número"}), 400

    # Verificar si el email es válido
    if not validate_email(email):
        return jsonify({"msg": "El correo electrónico no es válido"}), 400

    # Creamos el hash y lo almacenamos en la base de datos
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = User(username=username, password_hash=hashed_password, email=email, deviceID=deviceID, admin=False, profesor=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario registrado exitosamente"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('usernameOrEmail').strip()
    password = data.get('password').strip()
    deviceID = data.get('deviceID')

    # Verificar si el username_or_email es un nombre de usuario válido
    user = User.query.filter(User.username.ilike(username_or_email) | User.email.ilike(username_or_email)).first()

    if user:
        if bcrypt.check_password_hash(user.password_hash, password):
            # Verificar si el deviceID ha cambiado
            if user.deviceID != deviceID:
                user.deviceID = deviceID
                db.session.commit()

            # Creamos el token con el cual podrán mandar llamadas a la api
            access_token = create_access_token(identity=user.username)
            return jsonify(access_token=access_token, admin=user.admin), 200
        else:
            return jsonify({"msg": "La contraseña no es correcta"}), 401
    else:
        return jsonify({"msg": "Usuario inválido"}), 401

# Esta función sirve para ver si funciona tu token
@main.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

@main.route('/comprobar_sala', methods=['POST'])
def comprobar_sala():
    data = request.get_json()
    room = data.get('room')
    deviceID = data.get('deviceID')

    # Comprueba si la sala tiene un usuario asociado
    user = User.query.filter_by(despacho=room).first()
    if user:
        # Si la sala tiene un usuario asociado, comprueba el deviceID
        if user.deviceID != deviceID:
            print("DeviceID no coincide")
            admins = User.query.filter_by(admin=True).all()
            for admin in admins:
                print("Mensajes")
                msg = Message("Alerta de seguridad",
                              sender="shar3d.confirmaciones@gmail.com",
                              recipients=[admin.email])
                msg.body = f"El deviceID de la sala {room} no coincide con el registrado."
                mail.send(msg)

    return jsonify({"msg": "Comprobación de sala realizada"}), 200

@main.route('/cerrar_entradas', methods=['GET'])
@jwt_required()
def registrar_salidas():
    logging.info('Iniciando el registro de salidas')
    current_user = get_jwt_identity()

    if not current_user.is_admin:
            return jsonify({"msg": "No eres administrador"}), 403
        
    response = requests.get('https://api-mongo-9eqi.onrender.com/habitaciones/cerrar_entradas')
    logging.info('Respuesta de la API: %s', response.text)

    if response.status_code == 200:
        logging.info('Registro de salidas realizado con éxito')
        return jsonify({"msg": "Registro de salidas realizado con éxito"}), 200
    else:
        logging.error('Error al registrar salidas, código de estado: %s', response.status_code)
        return jsonify({"msg": "Error al registrar salidas"}), 500
    
@main.route('/send_email', methods=['POST'])
@jwt_required()
def send_email():
    
    if not request.is_json:
        return jsonify({"msg": "No hay JSON"}), 400

    subject = request.json.get('subject', None)
    body = request.json.get('body', None)
    
    current_user = get_jwt_identity()

    if not current_user.is_admin:
            return jsonify({"msg": "No eres administrador"}), 403
        
    if not subject or not body:
        return jsonify({"msg": "Debe haber asunto y mensaje"}), 400


    msg = Message(subject,
                  sender="shar3d.confirmaciones@gmail.com",
                  recipients=[user.email for user in User.query.all()])  # Asume que tienes un modelo de usuario con un campo de correo electrónico
    msg.body = body
    mail.send(msg)

    return jsonify({"msg": "Mensaje enviado"}), 200