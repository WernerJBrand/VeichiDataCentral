# VeichiDataCentral

**Veichi Central Hub** is a Django-based knowledge base designed for Veichi VFDs (Variable Frequency Drives). It provides a centralized platform for managing technical documentation, error codes, and models, featuring a public-facing search interface and a secure back-end for technicians.

## Features

-   **Public Search Interface:** comprehensive search for VFD models and error codes.
-   **Technician Dashboard:** Secure Django Admin interface for managing data.
-   **API Access:** REST API endpoints for external tools and integrations.
-   **Documentation Management:** Upload and organize manuals and technical guides.

## Prerequisites

-   macOS (or Linux/Windows with appropriate adjustments)
-   Python 3.10+
-   Terminal access

## Installation & Setup

Follow these steps to set up the project locally.

### 1. Create and Activate Virtual Environment

```bash
cd /path/to/VeichiDataCentral
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

Create the database tables based on the models:

```bash
python manage.py makemigrations hub
python manage.py migrate
```

### 4. Create Admin User

Create a superuser for the Technician Back-End:

```bash
python manage.py createsuperuser
```
*Follow the prompts to set a username, email, and password.*

### 5. Run the Server

```bash
python manage.py runserver
```

## Usage

Once the server is running, you can access the following:

1.  **Public Front-End:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    -   Use the search bar to find information on VFD models and errors.

2.  **Technician Back-End:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
    -   Log in with your superuser credentials.
    -   Manage `VFDModel`, `ErrorCode`, and other data.

3.  **API:** [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
    -   Explore available API endpoints for integration.