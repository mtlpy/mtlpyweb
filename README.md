# MontréalPython Website

## Deployment

Deployments are triggered automatically when pushing to the *master* branch.

## Development

Configure your local env file:

    $ cp .env.example .env

Build your dev docker image:

    $ docker-compose build

Run initial DB setup:

    $ docker-compose run web python manage.py syncdb --migrate
    $ docker-compose run web python manage.py loaddata fixtures/*

Run server:

    $ docker-compose up
