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
          'Django==1.5.1',
          'django-localeurl',
          'South',
          'sorl-thumbnail',
          'django-extensions',
          'markdown',
          'Pillow',
          'requests',
          'arrow',
          'python-memcached',
          'django-pagination',
          'google-api-python-client',
        ],
      )
