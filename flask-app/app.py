from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# Mock database
USERS = {
    'test@example.com': {
        'password': 'password123',
        'name': 'Test User',
    }
}

FILES = [
    {'id': 1, 'name': 'research_paper.pdf', 'size': '2.3 MB', 'user': 'test@example.com', 'date': '2024-01-15'},
    {'id': 2, 'name': 'data_analysis.csv', 'size': '1.1 MB', 'user': 'test@example.com', 'date': '2024-01-20'},
    {'id': 3, 'name': 'presentation.pptx', 'size': '5.2 MB', 'user': 'test@example.com', 'date': '2024-02-01'},
]

# Bug #1 fix: add a simple auth gate for routes that need a logged-in user
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        email = session.get('email')
        if not email or email not in USERS:
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = USERS.get(email)
        if user and user['password'] == password:
            session['email'] = email
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

# BUG #1: Fixed
@app.route('/dashboard')
@login_required
def dashboard():
    email = session.get('email')
    user = USERS.get(email)
    
    user_files = [f for f in FILES if f['user'] == email]
    
    return render_template('dashboard.html', 
                         user=user, 
                         files=user_files)

# BUG #2: Fixed
@app.route('/api/files')
@login_required
def get_files():
    if 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    email = session['email']
    
    # BUG #2 fix: Do the user lookup once and only filter the files we need, which would solve N+1 query problem
    user_name = USERS.get(email, {}).get('name', 'Unknown')
    user_files = [f for f in FILES if f['user'] == email]
    result = [
        {
            'id': f['id'],
            'name': f['name'],
            'size': f['size'],
            'date': f['date'],
            'user_name': user_name
        }
        for f in user_files
    ]
    
    return jsonify(result)

ALLOWED_EXTENSIONS = {'pdf', 'csv', 'pptx', 'xlsx', 'docx', 'txt'}
DANGEROUS_EXTENSIONS = {'exe', 'bat', 'cmd', 'com', 'js', 'jar', 'sh'}

def is_allowed_filename(filename: str) -> bool:
    if not filename:
        return False

    safe = secure_filename(filename)
    if not safe or safe.startswith('.'):
        return False

    # Split on dots and examine the chain: "malware.exe.pdf" -> ["malware", "exe", "pdf"]
    parts = safe.lower().split('.')
    if len(parts) < 2:
        return False

    ext = parts[-1]
    if ext not in ALLOWED_EXTENSIONS:
        return False

    # Reject if ANY intermediate extension is dangerous (blocks "something.exe.pdf")
    for maybe_ext in parts[1:-1]:
        if maybe_ext in DANGEROUS_EXTENSIONS:
            return False

    return True

# BUG #3: Fixed
@app.route('/upload', methods=['POST'])
@login_required
def upload():    
    filename = request.form.get('filename', '')
    
    if not is_allowed_filename(filename):
        return 'Invalid file', 400

    new_file = {
        'id': len(FILES) + 1,
        'name': secure_filename(filename),
        'size': '0.5 MB',
        'user': session['email'],
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    FILES.append(new_file)
    return redirect(url_for('dashboard'))

@app.route('/search')
@login_required
def search():    
    query = request.args.get('q', '').lower()
    email = session['email']
    
    user_files = [f for f in FILES if f['user'] == email]
    
    if query:
        filtered = [f for f in user_files if query in f['name'].lower()]
        return render_template('dashboard.html', 
                             user=USERS.get(email),
                             files=filtered,
                             search_query=query)
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
