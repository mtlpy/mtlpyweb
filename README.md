# MontréalPython Website

## Deployment

Deployments are triggered automatically when pushing to the *master* branch.

## [Code of Conduct](https://github.com/mtlpy/code-of-conduct)

Montréal-Python has adopted a Code of Conduct that we expect project
participants to adhere to. If you need more informations please read
[the full text](https://github.com/mtlpy/code-of-conduct) for an overview of the
types of behaviours deemed inappropriate. Please read so that you can understand
what actions will and will not be tolerated.

## Development

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

### Dependencies

The list of dependencies is maintained in `requirements.source.txt`.

The locked versions for deployment are in `requirements.txt`.

To update the locked versions:

    $ sudo docker-compose run web bash -c 'pip freeze > requirements.txt'

## License

The Montréal-Python is Apache licensed.
