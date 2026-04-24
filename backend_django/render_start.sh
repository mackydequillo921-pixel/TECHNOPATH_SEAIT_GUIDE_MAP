#!/bin/bash
# Render Start Script for Django Backend

# Run migrations
echo "Running migrations..."
python manage.py migrate --run-syncdb

# Seed all default admin accounts (safety_admin, all deans, all program heads)
echo "Seeding default admin accounts..."
python manage.py seed_admins

# Static files already collected during build
# Start gunicorn
echo "Starting Gunicorn..."
gunicorn technopath.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --threads 2 --timeout 60
