release: python manage.py migrate --noinput
web: python manage.py migrate --noinput && gunicorn Hello.wsgi:application --bind 0.0.0.0:$PORT
