from flask_restplus import Resource, Namespace

user_ns = Namespace('user')


@user_ns.route('/hello')
class HelloUser(Resource):
    def get(self):
        return {'hello': 'I am a user'}
