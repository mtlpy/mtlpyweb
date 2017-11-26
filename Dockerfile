FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN pip install -U 'pip > 9' pipenv

ADD . /app
WORKDIR /app

RUN pipenv install --deploy --system --verbose

# CMD python manage.py runserver 0.0.0.0:8000
CMD gunicorn mtlpy.wsgi:application --log-file - -b 0.0.0.0:8000

EXPOSE 8000
