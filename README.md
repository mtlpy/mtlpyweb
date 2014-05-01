============
mtlpy-django
============

# How to setup the environment:

- Install the packages `pip install -r requirements.txt`
- Setup the database by first editing `mtlpy.settings` and running `./manage.py syncdb --migrate`
- Import a base list of posts, categories and users `./manage.py loaddata db.json`
- Setup yourself as a superuser
    - Log in to the admin site as admin (password 'admin')
    - Set a password for yourself, or create your user account if it does not exist.
    - Set yourself as superuser
    - Log out and re-log into the admin as yourself
    - Delete admin account
- (Optional) Load the posts from the wordpress site (see 'Load from Wordpress' below)
- (Optional) import the sponsor.ini file by `./manage.py import_sponsors sponsor.ini`

Now you are ready to run the server `./manage.py runserver 0.0.0.0:8000`

Install instructions
--------------------

- Clone the repo on the server
- Run the bootstrap:
    - sudo make bootstrap
- Change directory to /opt/mp/website
- Run all make commands as root (run make to get the help)

Help! I am a user but I can't login!
------------------------------------

- You should already exist as a user, but you need an admin to change your password. Ask a friendly pre-existing admin to reset your password from the user page in django-admin.

How to compile the css
----------------------

- Install compass `gem install compass`
- Excute `compass compile` at the root folder (the one with the config.rb file)

Load from Wordpress
-------------------

First you will need a english and a french dump of the old wordpress site. Go to the export tool (http://montrealpython.org/wp-admin/export.php) and pick 'Posts', keep the other options as is. Then do the same but from http://montrealpython.org/wp-admin/export.php?lang=fr for the french dump.

Then, run the following manage.py command:

    ./manage.py import_xml EN_DUMP FR_DUMP

How to move blog posts from a set of categories to another category
-------------------------------------------------------------------

- Go to /en/blog/transfer_tool/
- Sign in with staff user
- Select "from" categories
- Select "to" category
- Blog posts in the "from" category will be moved to the "to" category.

How to ensure sponsor logos are converted to grayscale (and properly clear thumbnail cache):
--------------------------------------------------------------------------------------------

Sorl-thumbnail is used, you will need to clear thumbnail cache. Be careful, this contains rm -rf!!

- cd <website root>
- rm -rf mtlpy/media/cache/*
- python manage.py thumbnail clear
- python manage.py thumbnail cleanup
