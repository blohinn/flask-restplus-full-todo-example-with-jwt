from flask import Blueprint
from flask_restplus import Api, Resource

v1_blueprint = Blueprint('v1_blueprint', __name__)
v1_api = Api(v1_blueprint,
             title='TODO API',
             version='1.0',
             description='')

from .resources.auth import auth_ns
from .resources.todo import todo_ns
from .resources.user import user_ns

v1_api.add_namespace(auth_ns)
v1_api.add_namespace(todo_ns)
v1_api.add_namespace(user_ns)

