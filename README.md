# Cedar Support Hub (formerly Veichi Central Hub)

**Cedar Support Hub** is a centralized knowledge base and support tool designed to consolidate technical documentation, error codes, and models for various product lines, including **Veichi**, **Spitfire**, **Ceva**, and more. It serves as a single source of truth for technicians and support staff, offering a public-facing search interface and a secure back-end for data management.

## Purpose

The primary goal of Cedar Support Hub is to streamline the troubleshooting and support process by:
*   **Centralizing Data:** Aggregating manuals, fault codes, and product specifications from different manufacturers into one searchable database.
*   **Simplifying Access:** Providing a clean, intuitive web interface for technicians to quickly find relevant information.
*   **Standardizing Support:** Ensuring all support staff have access to the same up-to-date information.

## Key Features

-   **Multi-Product Search:** comprehensive search functionality that spans across all supported device families (Veichi, Spitfire, Ceva, etc.).
-   **Fault Code Lookup:** Quickly identify error codes and their solutions for specific models.
-   **Community Forum:** A space for technicians to ask questions and share knowledge, with built-in moderation.
-   **Smart Manuals:** Automatic OCR text extraction and AI tagging for uploaded manuals (with manual override capabilities).
-   **Technician Dashboard:** A secure Django Admin interface for authorized personnel to add, edit, or remove products, error codes, and forum posts.
-   **API Access:** REST API endpoints to allow other tools to query the knowledge base programmatically.

## How It Works

The application is built with **Django** (Python web framework) and uses a **SQLite** database for easy local deployment and portability.

### For General Users (Public Interface)
1.  **Launch the App:** Double-click the `Launch Cedar Support Hub.command` script.
2.  **Search:** Use the search bar on the home page to enter a product model (e.g., "AC10") or a fault code (e.g., "E.LuT").
3.  **View Results:** Click on the search results to see detailed information, including fault descriptions, possible causes, and solutions.
4.  **Browse Manuals:** Navigate to the "Manuals" section to download PDF documentation.

### For Technicians (Admin Backend)
1.  **Login:** Go to `/admin` or click "Technician Login" in the navigation bar.
2.  **Manage Data:**
    *   **VFD Models:** Add new drive models and associate them with their respective series/families.
    *   **Error Codes:** Input new fault codes, linking them to specific models.
    *   **Manuals:** Upload and categorize new PDF manuals.

## Installation & Setup (For Developers)

Use these steps if you are setting up the project from source or resetting the environment.

### Prerequisites
-   macOS (recommended) or Linux/Windows
-   Python 3.10+
-   Terminal access

### Quick Start
1.  **Clone/Download** the repository to your local machine.
2.  **Run the Setup:**
    ```bash
    cd VeichiDataCentral
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    # Install dependencies
    pip install -r requirements.txt
    # Initialize database
    python manage.py migrate
    # Create admin user
    python manage.py createsuperuser
    ```
3.  **Launch:**
    ```bash
    ./Launch\ Cedar\ Support\ Hub.command
    ```

## Project Structure
-   `hub/`: Main application logic (models, views, templates).
-   `veichi_central/`: Project configuration settings.
-   `templates/`: HTML templates for the front-end.
-   `static/` & `media/`: CSS, JS, and uploaded files (manuals).
-   `db.sqlite3`: The local database file.

---
© 2026 Cedar Solar