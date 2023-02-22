import unittest
from website import create_app
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

'''
class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True
    
    def test_flask_app(self):
        # Test that the Flask app is created successfully and returns a valid Flask instance
        self.assertIsInstance(self.app, Flask)

        # Test that the Flask app is running on the correct host and port
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

        # Test that the Flask app returns the correct response for different URLs and HTTP methods
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About Us', response.data)

if __name__ == '__main__':
    unittest.main()
'''
