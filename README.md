# Document Chatbot

A powerful AI-powered application that allows users to chat with their documents. Upload PDFs, TXT, DOC, or DOCX files and ask questions to get instant insights and information.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Web Browser    │◄────┤  Flask Server   │◄────┤  OpenRouter API │
│ (User Interface)│     │  (Backend)      │     │  (AI Model)     │
│                 │────►│                 │────►│                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │                 │
                        │  SQLite Database│
                        │  (Storage)      │
                        │                 │
                        └─────────────────┘
```

### How It Works:

1. **User uploads a document** through the web interface
2. **Document is stored** in the server's file system
3. **Text is extracted** from the document
4. **User asks questions** about the document
5. **Questions and document content** are sent to the AI model
6. **AI generates answers** based on the document content
7. **Answers are displayed** to the user in a chat interface

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Python, Flask
- **Database**: SQLite
- **AI Model**: Google's Gemma 3n 4B (via OpenRouter API)
- **Authentication**: Flask-Login
- **Document Processing**: PyPDF2 (for PDF extraction)
- **Environment Variables**: python-dotenv

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Installation Steps

1. **Clone the repository** (or download the ZIP file)
   ```
   git clone https://github.com/sangisetti-pavankumar/Document-chatbot.git
   cd document-chatbot
   ```

2. **Create a virtual environment** (optional but recommended)
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   - Create a `.env` file in the root directory with the following content:
     ```
     SECRET_KEY=your_secret_key_here
     OPENROUTER_API_KEY=your_openrouter_api_key
     SITE_URL=http://localhost:5000
     SITE_NAME=Document Chatbot
     ```
   - Get your OpenRouter API key from [OpenRouter](https://openrouter.ai/)

6. **Run the application**
   ```
   python app.py
   ```

7. **Access the application**
   - Open your web browser and go to `http://localhost:5000`
   - Login with the default admin account:
     - Username: `admin`
     - Password: `admin123`

## Usage

1. **Login** to the application
2. **Upload documents** (Admin only)
3. **View documents** on the dashboard
4. **Click on a document** to view its content
5. **Click "Chat with Document"** to start asking questions
6. **Type your questions** in the chat interface
7. **View chat history** for previous conversations

## Features

- **Document Management**: Upload, view, download, and delete documents
- **AI-Powered Chat**: Ask questions about document content
- **User Authentication**: Secure login and registration
- **Role-Based Access**: Admin and regular user roles
- **Responsive Design**: Works on desktop and mobile devices
- **Chat History**: Save and review previous conversations

## Rate Limits

The application uses OpenRouter API which has the following rate limits:
- 10 requests per 10 seconds on the free tier
- The application includes rate limiting to prevent errors

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [OpenRouter](https://openrouter.ai/)
- [Google's Gemma Model](https://ai.google.dev/gemma)
- [PyPDF2](https://pythonhosted.org/PyPDF2/)
