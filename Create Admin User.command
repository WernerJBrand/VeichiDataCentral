#!/bin/bash
cd "$(dirname "$0")"
echo "Creating Administrator Account for Veichi Hub..."
source venv/bin/activate
python manage.py createsuperuser
echo "Done! You can now log in at http://127.0.0.1:8000/admin/"
read -p "Press [Enter] to exit..."
