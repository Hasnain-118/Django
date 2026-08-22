web: gunicorn Hello.wsgi
release: python manage.py migrate