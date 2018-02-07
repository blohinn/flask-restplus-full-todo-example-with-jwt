from flask_restplus import fields
from sqlalchemy import ForeignKey
from ..resources.user import user_ns
from app import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    task = db.Column(db.String(50))
    done = db.Column(db.Boolean(False))

    todo_resource_model = user_ns.model('Todo', {
        'id': fields.Integer(readOnly=True, description='The task unique identifier. ReadOnly.'),
        'task': fields.String(required=True, description='The task details'),
        'done': fields.String(description='Bla bla bla')
    })
