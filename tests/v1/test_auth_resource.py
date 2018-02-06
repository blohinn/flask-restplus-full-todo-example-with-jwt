import tempfile
import unittest

import os
from flask import json

from app import create_app, db
from config import basedir


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
