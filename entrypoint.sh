#!/bin/sh

while ! nc -z "$DB_HOST" "$DB_PORT"; do
        echo "Database is still unavailable"
        sleep 1
done

python manage.py makemigrations
python manage.py migrate

make -C docs/ html

python -m gunicorn app.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
