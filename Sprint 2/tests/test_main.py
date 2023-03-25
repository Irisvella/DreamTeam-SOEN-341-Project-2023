'''
import unittest
from flask import url_for
from app import create_app, db
from app.models.user import Post, User
from sqlalchemy.sql import func


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(id='30', last_name='dsd', company_name='sad', phone_number='23432', resume_file='sfsdfd'.encode(), profile='fdfd', first_name='testuser', email='tfj@example.com', password='password')
            db.session.add(user)
            db.session.commit()
            post = Post(title='Test Post', text='This is a test post', company='test', address='234235', salary='3534', field='sdfwd', date_created=func.now())
            db.session.add(post)
            db.session.commit()


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.client.get(url_for('main.home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)
'''
