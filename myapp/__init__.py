# __init__.py
from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import db, bcrypt, jwt, mail
from .routes import main

load_dotenv() 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['BCRYPT_LOG_ROUNDS'] = 12
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'shar3d.confirmaciones@gmail.com'  # Reemplaza con tu correo
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')  # Reemplaza con tu contraseña
    
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    with app.app_context():
        db.drop_all()  # drop all tables
        db.create_all()
        
    app.register_blueprint(main)

    return app