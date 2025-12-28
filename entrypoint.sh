#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput


## for development only
#python manage.py runserver 0.0.0.0:8000 --nothreading --noreload
python manage.py runserver 0.0.0.0:8000 --nothreading

## alternative for development
# gunicorn wg_manage_project.wsgi:application --bind 0.0.0.0:8000 --workers=1 --timeout=300 --reload


