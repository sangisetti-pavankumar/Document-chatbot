import unittest
import os
import sys
import tempfile
import shutil

# Add parent directory to path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, init_db

class DocumentChatbotTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for uploads
        self.test_upload_dir = tempfile.mkdtemp()
        
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['UPLOAD_FOLDER'] = self.test_upload_dir
        
        # Create test client
        self.client = app.test_client()
    
    def tearDown(self):
        # Remove the temporary directory
        shutil.rmtree(self.test_upload_dir)
    
    def test_index_page(self):
        """Test that the index page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Document Chatbot', response.data)
    
    def test_login_page(self):
        """Test that the login page loads correctly"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_register_page(self):
        """Test that the register page loads correctly"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
    
    def test_dashboard_requires_login(self):
        """Test that dashboard requires login"""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        self.assertNotIn(b'Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()