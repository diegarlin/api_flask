# routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .extensions import bcrypt
from .models import User, db
import re

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
    
    new_user = User(username=username, password_hash=hashed_password, email=email, deviceID=deviceID)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario registrado exitosamente"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username_or_email = data.get('usernameOrEmail', '').strip()
    password = data.get('password', '').strip()
    deviceID = data.get('deviceID')

    if not username_or_email or not password:
        return jsonify({"msg": "El nombre de usuario/correo electrónico y la contraseña son obligatorios"}), 400

    # Verificar si el username_or_email es un nombre de usuario válido
    user = User.query.filter_by(username=username_or_email).first()

    # Si no encontramos un usuario con ese nombre de usuario, intentamos buscar por email
    if not user:
        user = User.query.filter_by(email=username_or_email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Nombre de usuario/correo electrónico o contraseña incorrectos"}), 401

    # Verificar si el deviceID ha cambiado
    if user.deviceID != deviceID:
        user.deviceID = deviceID
        db.session.commit()

    return jsonify({"msg": "Inicio de sesión exitoso"}), 200

# Esta función sirve para ver si funciona tu token
@main.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None