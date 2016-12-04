from setuptools import setup, find_packages

requirements = [
    'arrow',
    'boto',
    'dj-static==0.0.6',
    'django-environ==0.4.0',
    'django-extensions==1.1.1',
    'django-localeurl==1.5',
    'django-pagination==1.0.7',
    'django-storages',
    'Django-tinymce-filebrowser==0.1.1',
    'Django==1.5.4',
    'google-api-python-client==1.3.2',
    'gunicorn',
    'Markdown',
    'Pillow',
    'psycopg2==2.6.2',
    'requests',
    'sorl-thumbnail',
    'South==0.7.6',
    'oauth2client==3.0.0',  # Fix version for youtube?
]


setup(
    name='mtlpywebsite',
    version='0.0.0',
    description='Montreal Python',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='tuktu.tests',
    install_requires=requirements,
)
