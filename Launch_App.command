#!/bin/bash
# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Launch Browser in 2 seconds
(sleep 2 && open http://127.0.0.1:8000) &

# Run Server
source venv/bin/activate
python manage.py runserver
