from flask_restplus import Resource, Namespace

auth_ns = Namespace('auth')


@auth_ns.route('/hello')
class HelloAuth(Resource):
    def get(self):
        return {'hello': 'I am a auth'}