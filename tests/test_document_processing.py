import unittest
import os
import sys
import tempfile

# Add parent directory to path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import extract_text_from_file

class DocumentProcessingTestCase(unittest.TestCase):
    def setUp(self):
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temporary directory
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def test_extract_text_from_txt_file(self):
        """Test extracting text from a TXT file"""
        # Create a test TXT file
        test_content = "This is a test document.\nIt has multiple lines.\nTesting 1, 2, 3."
        test_file_path = os.path.join(self.test_dir, "test_document.txt")
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Extract text from the file
        extracted_text = extract_text_from_file(test_file_path)
        
        # Check that the extracted text matches the original content
        self.assertEqual(extracted_text, test_content)
    
    def test_extract_text_from_unsupported_file(self):
        """Test extracting text from an unsupported file type"""
        # Create a test file with unsupported extension
        test_file_path = os.path.join(self.test_dir, "test_document.xyz")
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write("Test content")
        
        # Extract text from the file (should return empty string)
        extracted_text = extract_text_from_file(test_file_path)
        
        # Check that the extracted text is empty
        self.assertEqual(extracted_text, "")

if __name__ == '__main__':
    unittest.main()