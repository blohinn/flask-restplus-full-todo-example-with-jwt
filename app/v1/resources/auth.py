from flask import current_app, request
from flask_restplus import Resource, Namespace, fields
from ..models.user import User
from ..models.auth import RefreshToken
from app import db
from app.v1 import v1_api
from ..exceptions import ValidationException
import re
import jwt
import datetime
import hashlib

auth_ns = Namespace('auth')

register_model = v1_api.model('Register', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

return_token_model = v1_api.model('ReturnToken', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
})


@auth_ns.route('/register')
class Register(Resource):
    # 4-16 symbols, can contain A-Z, a-z, 0-9, _ (_ can not be at the begin/end and can not go in a row (__))
    USERNAME_REGEXP = r'^(?![_])(?!.*[_]{2})[a-zA-Z0-9._]+(?<![_])$'

    # 6-64 symbols, required upper and lower case letters. Can contain !@#$%_  .
    PASSWORD_REGEXP = r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[\w\d!@#$%_]{6,64}$'

    @auth_ns.expect(register_model, validate=True)
    @auth_ns.marshal_with(User.user_resource_model)
    @auth_ns.response(400, 'username or password incorrect')
    def post(self):
        if not re.search(self.USERNAME_REGEXP, v1_api.payload['username']):
            raise ValidationException(error_field_name='username',
                                      message='4-16 symbols, can contain A-Z, a-z, 0-9, _ \
                                      (_ can not be at the begin/end and can not go in a row (__))')

        if not re.search(self.PASSWORD_REGEXP, v1_api.payload['password']):
            raise ValidationException(error_field_name='password',
                                      message='6-64 symbols, required upper and lower case letters. Can contain !@#$%_')

        if User.query.filter_by(username=v1_api.payload['username']).first():
            raise ValidationException(error_field_name='username', message='This username is already exists')

        user = User(username=v1_api.payload['username'], password=v1_api.payload['password'])
        db.session.add(user)
        db.session.commit()
        return user


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(200, 'Success', return_token_model)
    @auth_ns.response(401, 'Incorrect username or password')
    def post(self):
        """
        Look implementation notes
        This API implemented JWT. Token's payload contain:
        'uid' (user id),
        'exp' (expiration date of the token),
        'iat' (the time the token is generated)
        """
        user = User.query.filter_by(username=v1_api.payload['username']).first()
        if not user:
            auth_ns.abort(401, 'Incorrect username or password')

        from werkzeug.security import check_password_hash
        if check_password_hash(user.password_hash, v1_api.payload['password']):
            _access_token = jwt.encode({'uid': user.id,
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                                        'iat': datetime.datetime.utcnow()},
                                       current_app.config['SECRET_KEY']).decode('utf-8')
            _refresh_token = jwt.encode({'uid': user.id,
                                         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                                         'iat': datetime.datetime.utcnow()},
                                        current_app.config['SECRET_KEY']).decode('utf-8')

            user_agent_string = request.user_agent.string.encode('utf-8')
            user_agent_hash = hashlib.md5(user_agent_string).hexdigest()

            refresh_token = RefreshToken.query.filter_by(user_agent_hash=user_agent_hash).first()

            if not refresh_token:
                refresh_token = RefreshToken(user_id=user.id, refresh_token=_refresh_token,
                                             user_agent_hash=user_agent_hash)
            else:
                refresh_token.refresh_token = _refresh_token

            db.session.add(refresh_token)
            db.session.commit()
            return {'access_token': _access_token, 'refresh_token': _refresh_token}, 200

        auth_ns.abort(401, 'Incorrect username or password')


@auth_ns.route('/refresh')
class Refresh(Resource):
    @auth_ns.expect(v1_api.model('RefreshToken', {'refresh_token': fields.String(required=True)}), validate=True)
    @auth_ns.response(200, 'Success', return_token_model)
    def post(self):
        _refresh_token = v1_api.payload['refresh_token']

        try:
            payload = jwt.decode(_refresh_token, current_app.config['SECRET_KEY'])

            refresh_token = RefreshToken.query.filter_by(user_id=payload['uid'], refresh_token=_refresh_token).first()

            if not refresh_token:
                raise jwt.InvalidIssuerError

            # Generate new pair

            _access_token = jwt.encode({'uid': refresh_token.user_id,
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                                        'iat': datetime.datetime.utcnow()},
                                       current_app.config['SECRET_KEY']).decode('utf-8')
            _refresh_token = jwt.encode({'uid': refresh_token.user_id,
                                         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                                         'iat': datetime.datetime.utcnow()},
                                        current_app.config['SECRET_KEY']).decode('utf-8')

            refresh_token.refresh_token = _refresh_token
            db.session.add(refresh_token)
            db.session.commit()

            return {'access_token': _access_token, 'refresh_token': _refresh_token}, 200

        except jwt.ExpiredSignatureError as e:
            raise e
        except (jwt.DecodeError, jwt.InvalidTokenError)as e:
            raise e
        except:
            auth_ns.abort(401, 'Unknown token error')


from ..utils import token_required


# This resource only for test
@auth_ns.route('/protected')
class Protected(Resource):
    @token_required
    def get(self, current_user):
        return {'i am': 'protected', 'uid': current_user.id}
