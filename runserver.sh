#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py makemigrations main # Hotfix for makemigrations error
python manage.py migrate
gunicorn langchainApp.wsgi --bind=0.0.0.0:80 --timeout 300
