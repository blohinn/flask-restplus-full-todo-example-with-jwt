from flask_restplus import fields
from sqlalchemy import ForeignKey
from app import db
from app.v1 import v1_api


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    task = db.Column(db.String(50))
    done = db.Column(db.Boolean(), default=False)

    todo_resource_model = v1_api.model('Todo', {
        'id': fields.Integer(readOnly=True, description='The task unique identifier. ReadOnly.'),
        'task': fields.String(required=True, description='The task details'),
        'done': fields.Boolean(description='Bla bla bla')
    })
