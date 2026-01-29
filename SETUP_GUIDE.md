# Veichi Central Hub - Setup Guide

This project is a Django-based knowledge base for Veichi VFDs. It includes a public search interface and a secure technician dashboard.

## Prerequisites
- macOS
- Python 3.10+
- Terminal

## Terminal Command List

Copy and paste these commands into your terminal to set up the project from scratch.

### 1. Create and Activate Virtual Environment
```bash
cd /Users/cedarsolar/Desktop/VeichiDataCentral
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
# Create the database tables based on our models
python manage.py makemigrations hub
python manage.py migrate
```

### 4. Create Admin User
You will be prompted to set a username, email, and password. This is for the Technician Back-End.
```bash
python manage.py createsuperuser
```

### 5. Run the Server
```bash
python manage.py runserver
```

## Setup Verification

1. **Public Front-End**: Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. You should see the search bar.
2. **Technician Back-End**: Open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with the superuser you created.
   - Try adding a `VFDModel` (e.g., "AC310").
   - Try adding an `ErrorCode` linked to that model.
3. **API Check**: Open [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) to see the available API endpoints for your external tools.

## Next Steps
- Upload Manuals via the Admin panel.
- Use the API to push data from your harvester tool.
