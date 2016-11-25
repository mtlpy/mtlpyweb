FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ADD . /app/

