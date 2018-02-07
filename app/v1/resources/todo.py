from flask_restplus import Resource, Namespace

from app import db
from app.v1 import v1_api
from .auth import token_required
from ..models.todo import Todo as TodoModel

todo_ns = Namespace('todo')


@todo_ns.route('/')
class TodoList(Resource):
    @todo_ns.marshal_with(TodoModel.todo_resource_model)
    @token_required
    def get(self, current_user):
        """Get todos list"""
        tasks = TodoModel.query.filter_by(user=current_user).all()
        return tasks

    @todo_ns.expect(TodoModel.todo_resource_model, validate=True)
    @todo_ns.marshal_with(TodoModel.todo_resource_model)
    @token_required
    def post(self, current_user):
        """Create a new task"""
        task = v1_api.payload['task']
        try:
            done = v1_api.payload['done']
        except KeyError:
            done = False

        todo = TodoModel(task=task, done=done, user=current_user)
        db.session.add(todo)
        db.session.commit()
        return todo


@todo_ns.route('/<int:id>')
class Todo(Resource):
    @todo_ns.response(404, 'Todo not found or you don\'t have permission to view it')
    @todo_ns.marshal_with(TodoModel.todo_resource_model)
    @token_required
    def get(self, id, current_user):
        """Get one task"""
        todo = TodoModel.query.filter_by(user=current_user, id=id).first_or_404()
        return todo

    @todo_ns.response(404, 'Todo not found or you don\'t have permission to edit it')
    @todo_ns.expect(TodoModel.todo_resource_model, validate=True)
    @todo_ns.marshal_with(TodoModel.todo_resource_model)
    @token_required
    def put(self, id, current_user):
        """Get one todo"""
        task = v1_api.payload['task']
        try:
            done = v1_api.payload['done']
        except KeyError:
            done = False

        todo = TodoModel.query.filter_by(user=current_user, id=id).first_or_404()

        todo.task = task
        if 'done' in v1_api.payload:
            todo.done = v1_api.payload['done']

        db.session.add(todo)
        db.session.commit()

        return todo

    @todo_ns.response(404, 'Todo not found or you don\'t have permission to delete it')
    @todo_ns.response(204, 'Todo deleted')
    @token_required
    def delete(self, id, current_user):
        """Delete one todo"""
        todo = TodoModel.query.filter_by(user=current_user, id=id).first_or_404()

        db.session.delete(todo)
        db.session.commit()

        return '', 204
