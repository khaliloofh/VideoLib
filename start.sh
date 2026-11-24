#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate

if ! curl -s http://127.0.0.1:9900/ > /dev/null; then
    python manage.py runserver 9900 &
    sleep 2
fi

google-chrome-stable --app=http://127.0.0.1:9900/ --class=VideoLib