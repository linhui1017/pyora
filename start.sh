#!/bin/bash
# Start Gunicorn processes
# pip install -r ./requirements.txt

echo Starting Gunicorn.
exec gunicorn app:app \
    --bind 0.0.0.0:5000 \
    --workers 2
    --reload 1
