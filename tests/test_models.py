import unittest
import os
import sys
import sqlite3

# Add parent directory to path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test user
        self.user_id = 1
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.is_admin = False
        
        self.user = User(self.user_id, self.username, self.email, self.is_admin)
    
    def test_user_creation(self):
        """Test that a user can be created correctly"""
        self.assertEqual(self.user.id, self.user_id)
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.is_admin, self.is_admin)
    
    def test_user_is_authenticated(self):
        """Test that is_authenticated returns True"""
        self.assertTrue(self.user.is_authenticated)
    
    def test_user_is_active(self):
        """Test that is_active returns True"""
        self.assertTrue(self.user.is_active)
    
    def test_user_is_anonymous(self):
        """Test that is_anonymous returns False"""
        self.assertFalse(self.user.is_anonymous)
    
    def test_user_get_id(self):
        """Test that get_id returns the correct id"""
        self.assertEqual(self.user.get_id(), str(self.user_id))
    
    def test_admin_user(self):
        """Test that an admin user has is_admin=True"""
        admin_user = User(2, 'admin', 'admin@example.com', True)
        self.assertTrue(admin_user.is_admin)

if __name__ == '__main__':
    unittest.main()