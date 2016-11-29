import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(name='Montreal python',
      version='0.1',
      description='Montreal Python',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='George',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tuktu.tests',
      install_requires=[
          'arrow',
          'boto',
          'django-environ ',
          'django-extensions == 1.1.1',
          'django-localeurl == 1.5',
          'django-pagination == 1.0.7',
          'django-storages',
          'Django-tinymce-filebrowser == 0.1.1',
          'Django==1.5.4',
          'google-api-python-client',
          'gunicorn',
          'Markdown',
          'Pillow',
          'psycopg2',
          'requests',
          'sorl-thumbnail',
          'South == 0.7.6',
        ],
      )
