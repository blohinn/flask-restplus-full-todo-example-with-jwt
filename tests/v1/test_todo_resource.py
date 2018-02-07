import unittest
from flask import json
from app import create_app, db
from .test_auth_resource import AuthResourceTestCase


class TodoResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_type='test')
        self.client = create_app(config_type='test').test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def create(self, access_token, task, done=False):
        return self.client.post('/api/v1/todo/', data=json.dumps({
            'task': task,
            'done': done
        }), content_type='application/json', headers={
            'Authorization': 'Bearer ' + str(access_token)
        })

    def view_one(self, access_token, id):
        return self.client.get('/api/v1/todo/', data=json.dumps({'id': id}), content_type='application/json', headers={
            'Authorization': 'Bearer ' + str(access_token)
        })

    def test_create_than_view(self):
        AuthResourceTestCase.register(self, 'anon', 'aA1234!')

        rv = AuthResourceTestCase.login(self, 'anon', 'aA1234!')
        response = json.loads(rv.data.decode('utf-8'))
        access_token = response['access_token']

        rv = self.create(access_token=access_token, task='write more tests')
        assert b'write more tests' in rv.data

        rv = self.view_one(access_token=access_token, id=1)
        assert b'write more tests' in rv.data

    # TODO Delete, Put, view_list test...
