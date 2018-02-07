from flask_restplus import Resource, Namespace
from .auth import token_required
from ..models.todo import Todo

todo_ns = Namespace('todo')


# TODO Сделать переменную current_user

@todo_ns.route('/')
class Todo(Resource):
    @todo_ns.marshal_with([Todo.todo_resource_model])
    @token_required
    def get(self):
        """Shows a list of all todos"""
        return {'hello': 'I am a todo'}

    @todo_ns.expect(Todo.todo_resource_model, validate=True)
    @todo_ns.marshal_with(Todo.todo_resource_model)
    @token_required
    def post(self):
        """Create a new task"""
        return {}

