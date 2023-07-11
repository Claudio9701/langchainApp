#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
gunicorn langchainApp.wsgi --bind=0.0.0.0:80