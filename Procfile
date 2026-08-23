release: python manage.py migrate --noinput
web: gunicorn Hello.wsgi:application --bind 0.0.0.0:$PORT
