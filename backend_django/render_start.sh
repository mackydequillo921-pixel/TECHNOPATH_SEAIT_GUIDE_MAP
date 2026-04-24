#!/bin/bash
# Render Start Script for Django Backend

# Run migrations
echo "Running migrations..."
python manage.py migrate --run-syncdb

# Create superuser if it doesn't exist (optional - for initial setup)
echo "from apps.users.models import AdminUser; AdminUser.objects.filter(username='admin').exists() or AdminUser.objects.create_superuser('admin', 'admin123', email='admin@example.com')" | python manage.py shell

# Static files already collected during build
# Start gunicorn
echo "Starting Gunicorn..."
gunicorn technopath.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --threads 2 --timeout 60
