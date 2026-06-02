release: python manage.py migrate
web: gunicorn mustangroundupsite.wsgi --bind 0.0.0.0:${PORT:-8000} --log-file -
