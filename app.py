import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
from datetime import datetime
import requests
import json
import PyPDF2
import io
import os
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size
app.config['DATABASE'] = 'database.db'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'doc', 'docx'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database initialization
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create documents table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        original_filename TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_type TEXT NOT NULL,
        uploaded_by INTEGER NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (uploaded_by) REFERENCES users (id)
    )
    ''')
    
    # Create chat history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        document_id INTEGER NOT NULL,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (document_id) REFERENCES documents (id)
    )
    ''')
    
    # Create default admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_password = generate_password_hash('admin123')
        cursor.execute("INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
                      ('admin', admin_password, 'admin@example.com', True))
    
    conn.commit()
    conn.close()

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email, is_admin):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_admin FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], bool(user_data[3]))
    return None

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Extract text from uploaded documents
def extract_text_from_file(file_path):
    file_ext = file_path.rsplit('.', 1)[1].lower()
    
    if file_ext == 'pdf':
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
        return text
    
    elif file_ext == 'txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    elif file_ext in ['doc', 'docx']:
        # For simplicity, we're not implementing doc/docx parsing
        # You would need python-docx or similar library for this
        return "Document text extraction not implemented for this file type."
    
    return ""

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, email, is_admin FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1], user_data[3], bool(user_data[4]))
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        
        # Check if username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            conn.close()
            flash('Username or email already exists', 'danger')
            return render_template('register.html')
        
        # Create new user (regular user, not admin)
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
                      (username, email, hashed_password, False))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Get all documents
    cursor.execute("""
        SELECT d.id, d.original_filename, d.file_type, d.uploaded_at, u.username 
        FROM documents d
        JOIN users u ON d.uploaded_by = u.id
    """)
    documents = cursor.fetchall()
    
    # Get document count
    cursor.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]
    
    # Get chat count for current user
    cursor.execute("SELECT COUNT(*) FROM chat_history WHERE user_id = ?", (current_user.id,))
    chat_count = cursor.fetchone()[0]
    
    # If admin, get user list and total users count
    users = []
    user_count = 0
    if current_user.is_admin:
        cursor.execute("SELECT id, username, email, is_admin, created_at FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
    
    conn.close()
    
    stats = {
        'documents': doc_count,
        'chats': chat_count,
        'users': user_count
    }
    
    return render_template('dashboard.html', documents=documents, users=users, stats=stats)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_document():
    if not current_user.is_admin:
        flash('Only admins can upload documents', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if 'document' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['document']
        
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            file_type = filename.rsplit('.', 1)[1].lower()
            
            conn = sqlite3.connect(app.config['DATABASE'])
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO documents (filename, original_filename, file_path, file_type, uploaded_by)
                VALUES (?, ?, ?, ?, ?)
            """, (unique_filename, filename, file_path, file_type, current_user.id))
            conn.commit()
            conn.close()
            
            flash('Document uploaded successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('File type not allowed', 'danger')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/document/<int:document_id>')
@login_required
def view_document(document_id):
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.id, d.original_filename, d.file_path, d.file_type, d.uploaded_at, u.username 
        FROM documents d
        JOIN users u ON d.uploaded_by = u.id
        WHERE d.id = ?
    """, (document_id,))
    document = cursor.fetchone()
    conn.close()
    
    if not document:
        flash('Document not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # Extract text from document for display
    document_text = extract_text_from_file(document[2])
    
    return render_template('document.html', document=document, document_text=document_text)

@app.route('/document/<int:document_id>/download')
@login_required
def download_document(document_id):
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute("SELECT filename, original_filename, file_path FROM documents WHERE id = ?", (document_id,))
    document = cursor.fetchone()
    conn.close()
    
    if not document:
        flash('Document not found', 'danger')
        return redirect(url_for('dashboard'))
    
    return send_from_directory(
        os.path.dirname(document[2]),
        os.path.basename(document[2]),
        as_attachment=True,
        download_name=document[1]
    )

@app.route('/document/<int:document_id>/delete', methods=['POST'])
@login_required
def delete_document(document_id):
    if not current_user.is_admin:
        flash('Only admins can delete documents', 'danger')
        return redirect(url_for('dashboard'))
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Get document info
    cursor.execute("SELECT file_path FROM documents WHERE id = ?", (document_id,))
    document = cursor.fetchone()
    
    if document:
        # Delete file from filesystem
        try:
            os.remove(document[0])
        except:
            pass
        
        # Delete from database
        cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        cursor.execute("DELETE FROM chat_history WHERE document_id = ?", (document_id,))
        conn.commit()
        flash('Document deleted successfully', 'success')
    else:
        flash('Document not found', 'danger')
    
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/chat/<int:document_id>', methods=['GET', 'POST'])
@login_required
def chat(document_id):
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Get document info
    cursor.execute("""
        SELECT d.id, d.original_filename, d.file_path 
        FROM documents d
        WHERE d.id = ?
    """, (document_id,))
    document = cursor.fetchone()
    
    if not document:
        conn.close()
        flash('Document not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get chat history
    cursor.execute("""
        SELECT query, response, timestamp
        FROM chat_history
        WHERE user_id = ? AND document_id = ?
        ORDER BY timestamp ASC
    """, (current_user.id, document_id))
    chat_history = cursor.fetchall()
    
    conn.close()
    
    return render_template('chat.html', document=document, chat_history=chat_history)

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data = request.json
    document_id = data.get('document_id')
    query = data.get('query')
    
    if not document_id or not query:
        return jsonify({'error': 'Missing document_id or query'}), 400
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Get document content
    cursor.execute("SELECT file_path FROM documents WHERE id = ?", (document_id,))
    document = cursor.fetchone()
    
    if not document:
        conn.close()
        return jsonify({'error': 'Document not found'}), 404
    
    # Extract text from document
    document_text = extract_text_from_file(document[0])
    
    # Call Gemma 3n 4B model via OpenRouter API
    try:
        openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        if not openrouter_api_key or openrouter_api_key == 'your_openrouter_api_key_here':
            return jsonify({'error': 'OpenRouter API key not configured'}), 500
            
        site_url = os.getenv('SITE_URL', 'http://localhost:5000')
        site_name = os.getenv('SITE_NAME', 'Document Chatbot')
        
        print(f"Using API key: {openrouter_api_key[:5]}...")
        print(f"Document text length: {len(document_text)}")
        print(f"Query: {query}")
        
        # Prepare a simpler payload for the API
        payload = {
            "model": "google/gemma-3n-e4b-it:free",
            "messages": [
                {
                    "role": "user",
                    "content": f"Answer this question based on the document: {query}"
                }
            ]
        }
        
        print(f"Request payload: {json.dumps(payload)[:200]}...")
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": site_url,
                "X-Title": site_name,
            },
            json=payload,
            timeout=30,  # Add timeout to prevent hanging
            verify=False  # Disable SSL verification
        )
        
        print(f"API Response status: {response.status_code}")
        response.raise_for_status()  # Raise exception for HTTP errors
        
        response_data = response.json()
        print(f"API Response data: {json.dumps(response_data)[:200]}...")
        
        if 'choices' not in response_data or len(response_data['choices']) == 0:
            error_msg = "Invalid response from API: 'choices' not found"
            print(error_msg)
            return jsonify({'error': error_msg}), 500
            
        if 'message' not in response_data['choices'][0]:
            error_msg = "Invalid response from API: 'message' not found in choices"
            print(error_msg)
            return jsonify({'error': error_msg}), 500
            
        if 'content' not in response_data['choices'][0]['message']:
            error_msg = "Invalid response from API: 'content' not found in message"
            print(error_msg)
            return jsonify({'error': error_msg}), 500
            
        ai_response = response_data['choices'][0]['message']['content']
        
        # Save to chat history
        cursor.execute("""
            INSERT INTO chat_history (user_id, document_id, query, response)
            VALUES (?, ?, ?, ?)
        """, (current_user.id, document_id, query, ai_response))
        conn.commit()
        conn.close()
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")
        conn.close()
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        conn.close()
        return jsonify({'error': f'Invalid API response format: {str(e)}'}), 500
    except Exception as e:
        print(f"General exception: {str(e)}")
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)