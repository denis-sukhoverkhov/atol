import json

from main import app, db, User
from unittest import TestCase


class TestUserApi(TestCase):
    def setUp(self):
        self.app = app.test_client()
        User.query.delete()

    def test_create_user(self):
        first_user = User.query.first()
        self.assertIsNone(first_user)

        with app.test_client() as client:
            data = {'name': 'Denis', 'age': 26}
            response = json.loads(client.post('/user', data=data).data.decode('utf-8'))

        first_user = User.query.first()

        self.assertEqual(first_user.name, data['name'])
        self.assertEqual(first_user.age, data['age'])

    def test_get_user_info(self):
        user = User(name='Vladimir', age=34)
        db.session.add(user)
        db.session.commit()

        with app.test_client() as client:
            response = json.loads(client.get('/user').data.decode('utf-8'))
        first = response[0]
        self.assertEqual(first['name'], user.name)
        self.assertEqual(first['age'], user.age)
        self.assertIsNotNone(first['register_date'])
        self.assertIsNotNone(first['last_activity'])
