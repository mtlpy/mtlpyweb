=========================
Scripts for MtlPy website
=========================

Installation
============

- pandoc
   - apt-get install pandoc
   - http://johnmacfarlane.net/pandoc/


Usage
=====

   scripts/wordpress.py -o data/ -m markdown_strict ~/montrealpython.xml


Bootstrap the mtlpy website
===========================

- ./manage.py syncdb --migrate
- ./manage.py createsuperuser # create the admin user (needed as fallback user for import)
- ./manage.py import_markdown --rootpath data
