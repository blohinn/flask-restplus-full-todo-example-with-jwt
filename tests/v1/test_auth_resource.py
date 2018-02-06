import unittest
from flask import json
from app import create_app, db


class AuthResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_type='test')
        self.client = create_app(config_type='test').test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def register(self, username, password):
        return self.client.post('/api/v1/auth/register', data=json.dumps({
            'username': username,
            'password': password
        }), content_type='application/json')

    def login(self, username, password):
        return self.client.post('/api/v1/auth/login', data=json.dumps({
            'username': username,
            'password': password
        }), content_type='application/json')

    def request_to_protected(self, access_token):
        return self.client.get('/api/v1/auth/protected', content_type='application/json', headers={
            'Authorization': 'Bearer ' + str(access_token)
        })

    def test_register(self):
        rv = self.register(None, '')
        assert b'errors' in rv.data
        assert b'Input payload validation failed' in rv.data

        rv = self.register('', None)
        assert b'errors' in rv.data
        assert b'Input payload validation failed' in rv.data

        rv = self.register('', '')
        assert b'errors' in rv.data
        assert b'4-16 symbols, can contain' in rv.data

        rv = self.register('vasek', '')
        assert b'errors' in rv.data
        assert b'6-64 symbols, required upper and lower case letters. Can contain !@#$%_' in rv.data

        rv = self.register('anon', '123')
        assert b'errors' in rv.data
        assert b'6-64 symbols, required upper and lower case letters. Can contain !@#$%_' in rv.data

        rv = self.register('anon', 'aA1234!')
        assert b'username' in rv.data
        assert b'anon' in rv.data

    def test_login(self):
        self.register('anon', 'aA1234!')

        rv = self.login('anon', 'aA1234!')
        assert b'access_token' in rv.data
        assert b'refresh_token' in rv.data

        rv = self.login('anon', 'incorrect_pass')
        assert b'Incorrect username or password' in rv.data

    def test_token_required(self):
        self.register('anon', 'aA1234!')

        rv = self.login('anon', 'aA1234!')
        response = json.loads(rv.data.decode('utf-8'))

        access_token = response['access_token']

        rv = self.request_to_protected(access_token)
        assert b'i am' in rv.data
        assert b'protected' in rv.data

        # expired access token:
        exp_at = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsImV4cCI6MTUxLCJpYXQiOjEyfQ.Jf4nIuqbfwRtB-K_yEDQ1sJHZWShkp5mDetWtVUcVqk'
        rv = self.request_to_protected(exp_at)
        assert b'expired' in rv.data

        # try without token
        rv = self.client.get('/api/v1/auth/protected', content_type='application/json')
        assert b'required' in rv.data

    def test_refreshing_token(self):
        self.register('anon', 'aA1234!')

        rv = self.login('anon', 'aA1234!')
        response = json.loads(rv.data.decode('utf-8'))
        access_token = response['access_token']
        refresh_token = response['refresh_token']

        rv = self.request_to_protected(access_token)
        assert b'i am' in rv.data
        assert b'protected' in rv.data

        import time
        time.sleep(1)

        rv = self.client.post('/api/v1/auth/refresh', data=json.dumps({
            'refresh_token': refresh_token
        }), content_type='application/json')

        response = json.loads(rv.data.decode('utf-8'))
        _access_token = response['access_token']
        _refresh_token = response['refresh_token']

        assert access_token != _access_token
        assert refresh_token != _refresh_token
