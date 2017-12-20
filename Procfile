release: python manage.py migrate --fake-initial
web: gunicorn --threads 4 mtlpy.wsgi --log-file -
