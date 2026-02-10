#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Cedar Support Hub..."
source venv/bin/activate
(sleep 2 && open "http://127.0.0.1:8000") &
python manage.py runserver
