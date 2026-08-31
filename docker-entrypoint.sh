#!/bin/sh
set -e

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Seeding demo content..."
python manage.py seed_demo

echo "==> Ensuring admin superuser..."
python manage.py shell -c "
import os
from django.contrib.auth.models import User
u = os.environ.get('DJANGO_SUPERUSER_USERNAME') or 'admin'
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, os.environ.get('DJANGO_SUPERUSER_EMAIL') or 'admin@example.com', os.environ.get('DJANGO_SUPERUSER_PASSWORD') or 'admin123')
    print('Superuser created:', u)
else:
    print('Superuser already exists:', u)
"

echo "==> Starting server..."
exec "$@"
