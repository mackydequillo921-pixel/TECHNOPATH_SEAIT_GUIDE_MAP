#!/bin/bash
# Render Start Script for Django Backend

# Run migrations
echo "Running migrations..."
python manage.py migrate --run-syncdb

# Seed all default admin accounts (safety_admin, all deans, all program heads)
echo "Seeding default admin accounts..."
python manage.py seed_admins

# Reset all passwords to admin123 (ensures password updates)
echo "Resetting all admin passwords..."
python manage.py reset_all_passwords

# Seed all facilities, rooms, navigation nodes, FAQ entries, etc.
echo "Seeding default campus data..."
python manage.py seed_default_data

# Seed navigation paths and nodes (using fixed model structure)
echo "Seeding navigation data..."
python manage.py seed_data_fixed || echo "Navigation seeding may have already run"

# Static files already collected during build
# Start gunicorn
echo "Starting Gunicorn..."
gunicorn technopath.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --threads 2 --timeout 60
