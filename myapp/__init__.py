# __init__.py
from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import db, bcrypt, jwt
from .routes import main

load_dotenv() 

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['BCRYPT_LOG_ROUNDS'] = 12

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(main)

    return app