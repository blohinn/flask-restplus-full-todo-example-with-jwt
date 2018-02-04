from flask_restplus import Resource, Namespace

todo_ns = Namespace('todo')


@todo_ns.route('/hello')
class HelloTodo(Resource):
    def get(self):
        return {'hello': 'I am a todo'}
