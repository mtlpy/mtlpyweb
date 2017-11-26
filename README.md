# Montréal-Python Website [🔗](https://montrealpython.org)

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

Start the services:

    $ docker-compose up

Run initial DB setup:

    $ pipenv run python manage.py migrate
    $ pipenv run python manage.py loaddata fixtures/00{1,2,3,4}_*.json

### Dependencies

We use [Pipenv](https://docs.pipenv.org/) to track the dependencies.

Some useful commands:

Setup the virtualenv and install the locked dependencies:
```bash
$ pipenv install
```

Run a command in the virtualenv:
```bash
$ pipenv run python manage.py runserver
```

Install a new dependency:
```bash
$ pipenv install 'requests'
```

For development dependencies:
```bash
$ pipenv install --dev 'pytest'
```

Update the `Pipfile.lock` file:
```bash
$ pipenv lock
```

Display a graph of the installed packages and their dependency relationships:
```bash
$ pipenv graph # --reverse
```

## Deployment

Continuous deployments is enabled on the *master* branch.

## License

The Montréal-Python website is Apache licensed.
