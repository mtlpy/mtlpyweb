FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN pip install -U 'pip > 9'

RUN mkdir /app
WORKDIR /app

ADD requirements.source.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.source.txt

ADD . /app/

CMD python manage.py runserver 0.0.0.0:8000

EXPOSE 8000
