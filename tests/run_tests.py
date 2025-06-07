import unittest
import sys
import os

# Add parent directory to path so we can import the tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test modules
from tests.test_routes import DocumentChatbotTestCase
from tests.test_models import UserModelTestCase
from tests.test_document_processing import DocumentProcessingTestCase

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(DocumentChatbotTestCase))
    test_suite.addTest(unittest.makeSuite(UserModelTestCase))
    test_suite.addTest(unittest.makeSuite(DocumentProcessingTestCase))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)