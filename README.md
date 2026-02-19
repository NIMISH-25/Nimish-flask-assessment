# Flask File Manager - Assessment

A simple file management application with intentional bugs for debugging practice.

## Setup Instructions

### 1. Install Python
Make sure you have Python 3.9 or higher installed:
```bash
python --version
# or
python3 --version
```

### 2. Install Dependencies
```bash
cd flask-app
pip install -r requirements.txt
# or if using python3
pip3 install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
# or
python3 app.py
```

### 4. Open in Browser
Visit: http://localhost:5000

### 5. Login
Use these test credentials:
- Email: test@example.com
- Password: password123

## Features

- User login/logout
- Dashboard showing uploaded files
- File upload (simulated)
- Search functionality

## Your Task

This app has **3 bugs** that you need to find and fix. See the assessment document for details.

## Troubleshooting

**Port already in use?**
```bash
# Kill process on port 5000 (Mac/Linux)
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Module not found?**
Make sure Flask is installed:
```bash
pip install Flask
```

**Permission denied?**
Use pip3 or add --user flag:
```bash
pip3 install -r requirements.txt
# or
pip install --user -r requirements.txt
```
