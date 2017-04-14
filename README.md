# MontréalPython Website [🔗](https://montrealpython.org)

## Code of Conduct

Montréal-Python has adopted a Code of Conduct that we expect project
participants to adhere to. If you need more informations please read
[the full text](https://github.com/mtlpy/code-of-conduct) for an overview of the types of behaviours deemed inappropriate. Please read so that you can understand what actions will and will not be tolerated.

[Code of conduct](https://github.com/mtlpy/code-of-conduct)

## Development

[![CircleCI](https://circleci.com/gh/mtlpy/mtlpyweb.svg?style=svg)](https://circleci.com/gh/mtlpy/mtlpyweb)

Configure your local env file:

    $ cp .env.example .env

To get a complete setup you'll also need to obtain a valid YOUTUBE_API_KEY.

Build your dev docker image:

    $ docker-compose build

Run initial DB setup:

    $ docker-compose run web python manage.py syncdb --migrate
    $ docker-compose run web python manage.py loaddata fixtures/*

Run server:

    $ docker-compose up

Erase your instance:

    $ docker-compose kill

### Dependencies

The list of dependencies is maintained in `requirements.source.txt`.

The locked versions for deployment are in `requirements.txt`.

To update the locked versions:

    $ docker-compose run -T web pip freeze | sort > requirements.txt

## Deployment

Continuous deployments is enabled on the *master* branch.

## License

The The Montréal-Python website is Apache licensed.
