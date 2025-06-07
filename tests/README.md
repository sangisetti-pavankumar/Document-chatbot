# Document Chatbot Tests

This directory contains simple test cases for the Document Chatbot application.

## Test Structure

- `test_routes.py`: Tests for basic Flask routes and page rendering
- `test_models.py`: Tests for the User model
- `test_document_processing.py`: Tests for document text extraction
- `run_tests.py`: Script to run all tests

## Running Tests

To run all tests:

```
python tests/run_tests.py
```

To run a specific test file:

```
python -m unittest tests/test_routes.py
```

## Test Coverage

These tests cover:

1. **Basic Routes**
   - Index page loads correctly
   - Login page loads correctly
   - Register page loads correctly
   - Dashboard requires authentication

2. **User Model**
   - User creation works correctly
   - User properties are set correctly
   - Admin flag works correctly

3. **Document Processing**
   - Text extraction from TXT files works
   - Handling of unsupported file types

## Adding New Tests

To add new tests:

1. Create a new test file in the `tests` directory
2. Import the necessary modules from the main application
3. Create a test class that inherits from `unittest.TestCase`
4. Add test methods that start with `test_`
5. Add your test class to `run_tests.py`