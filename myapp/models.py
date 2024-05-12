# models.py
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    deviceID = db.Column(db.String(120), nullable=False)
    profesor = db.Column(db.Boolean, nullable=True, default=None)
    despacho = db.Column(db.String(10), nullable=True, default=None)
    
    def update(self, changes):
        for field, value in changes.items():
            if hasattr(self, field):
                setattr(self, field, value)
        db.session.commit()
        
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'admin': self.admin,
            'deviceID': self.deviceID,
            'profesor': self.profesor,
            'despacho': self.despacho
        }