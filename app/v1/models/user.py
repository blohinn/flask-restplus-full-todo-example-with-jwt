from flask_restplus import fields
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from ..resources.user import user_ns
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(80))
    from .auth import RefreshToken
    refresh_tokens = relationship('RefreshToken', uselist=False, backref='user')

    @property
    def password(self):
        raise AttributeError('Password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    user_resource_model = user_ns.model('User', {
        'username': fields.String(required=True)
    })
