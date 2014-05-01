===========================
Bootstrap the mtlpy website
===========================


Mtlpy website has 2 deployments:

- /opt/mp/website-prod
- /opt/mp/website-prod

All commands are targetting prod.

The posts must be exported from wordpress, converted in fixtures before the
big migrations (conversion is using pandoc : too old on the server)

Notes:

- Don't forget to activate the virtualenv: source bin/activate
- Don't forget to source the envvar: source env.sh


Prepare Blog fixture
====================

Export posts ::

   -> Go to http://montrealpython.org/wp-admin/export.php
   -> Export "All content" to dumps/montrealpython.wordpress.xml


Import posts ::

   # # Requires pandoc 1.10+ https://launchpad.net/ubuntu/+source/pandoc
   # scripts/wordpress.py -o import_post/ -m markdown_strict montrealpython.wordpress.*.xml
   # ./manage.py import_markdown --rootpath import_post
   # ./manage.py dumpdata --indent 2 blog > fixtures/001_blog.json
   # git commit fixtures/001_blog.json


Initial Deployment steps
========================

Create the deployment environment ::

   # mkdir -p /opt/mp
   # git clone git@github.com:mtlpy/mtlpy-django.git /opt/mp/website-prod
   # virtualenv /opt/mp/website-prod
   # cd /opt/mp/website-prod


Install service ::

   # cp debian/upstart-prod /etc/init/website-prod.conf


Install nginx config ::

   # cp debian/nginx-prod /etc/nginx/sites-enabled/website-prod


Create environment variables ::

   # cp env.sh.example env.sh
   # pwgen -s 12 # Generate a mysql password
   # pwgen -s 32 # Generate a django secret key
   # vim env.sh


Create the database ::

   # mysql
   mysql> create database website_prod DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
   mysql> grant all on website_prod.* to website_prod@'localhost' identified by '__changeme__';
   mysql> flush privileges;


Install dependencies ::

   # . bin/activate
   (website-prod) # pip install --upgrade distribute mysql-python gunicorn setproctitle -r requirements.txt


Initialize DB ::

   (website-prod) # . env.sh
   (website-prod) # ./manage.py syncdb --migrate
   (website-prod) # ./manage.py loaddata fixtures/000_users.json
   (website-prod) # ./manage.py loaddata fixtures/001_blog.json
   (website-prod) # ./manage.py loaddata fixtures/002_pages.json
   (website-prod) # ./manage.py loaddata fixtures/003_sponsors.json


Prepare static for production ::

   (website-prod) # . env.sh
   (website-prod) # ./manage.py collectstatic


Start the service ::

   $ sudo start website-prod


Reload Nginx ::

   $ sudo service nginx reload


Upgrade Deployment steps
========================

Prepare for deployment ::

   # cd /opt/mp/website-prod
   # . bin/activate
   (website-prod) # . env.sh
   (website-prod) # git pull
   (website-prod) # pip install -r requirements.txt
   (website-prod) # ./manage.py syncdb --migrate
   (website-prod) # ./manage.py collectstatic


Restart the application ::

   # sudo restart website-prod
   
   
When life gives you lemons ::

   # status website-prod
   (website-prod) # tail log/error.log

