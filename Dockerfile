FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN pip install -U 'pip > 9'

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD . /app/

