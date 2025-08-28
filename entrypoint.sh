#!/bin/bash
# filepath: /home/minh/ecommerce/entrypoint.sh

set -e

echo "Starting Django application..."

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 0.1
done
echo "Database started"


# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created')
else:
    print(f'Superuser {username} already exists')
END

# Start server
echo "Starting server..."
if [ "$DEBUG" = "True" ]; then
    echo "Running in DEBUG mode"
    python manage.py runserver 0.0.0.0:8000
else
    echo "Running in PRODUCTION mode"
    python -m gunicorn --bind 0.0.0.0:8000 --workers 3 ecommerce.wsgi:application
fi