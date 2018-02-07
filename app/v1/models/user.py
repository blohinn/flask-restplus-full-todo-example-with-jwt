from flask_restplus import fields
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from app.v1 import v1_api
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(80))
    from .auth import RefreshToken
    refresh_tokens = relationship('RefreshToken', backref='user')
    from .todo import Todo
    todos = relationship('Todo', backref='user')

    @property
    def password(self):
        raise AttributeError('Password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    user_resource_model = v1_api.model('User', {
        'username': fields.String(required=True)
    })
