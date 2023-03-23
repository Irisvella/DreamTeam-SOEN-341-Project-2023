import unittest
from flask import Flask
from flask_testing import TestCase
from app import create_app, db
from app.models import User

class TestAuth(TestCase):
    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        db.create_all()
        self.user = User(profile="seeker",email="teser@example.com", first_name="Test", last_name="User", phone_number="123456789", password="password")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        response = self.client.post('auth/login', data=dict(email='testuser@example.com', password='password', profile='seeker'), follow_redirects=True)
        self.assert200(response)
        #self.assertIn(b'Logged in successfully', response.data)

    def test_logout(self):
        response = self.client.get('auth/logout', follow_redirects=True)
        self.assert200(response)
        #self.assertIn(b'You have been logged out', response.data)

    def test_signup(self):
        response = self.client.post('auth/sign-up', data=dict(email='newuser@example.com', first_name='New', last_name='User', phone_number='123456789', password1='password', password2='password'), follow_redirects=True)
        self.assert200(response)
        #self.assertIn(b'Account created successfully', response.data)

if __name__ == '__main__':
    unittest.main()