============================
README Environment Variables
============================

The django settings defaults to development config. To get a production
(or staging) configuration, you must set those environment variables ::

   GUNICORN_PORT=8001
   DEBUG="false"
   SECRET_KEY="XXXXXXXXXX"
   ALLOWED_HOSTS=""
   DATABASE_ENGINE="django.db.backends.mysql"
   DATABASE_NAME="website"
   DATABASE_USER="website"
   DATABASE_PASSWORD="donttellthensa"
   DATABASE_HOST=""
   DATABASE_PORT=""
   YOUTUBE_API_KEY="NVmnFlQvQHusn64TpCDEXG6cpRZQ9rvqc7lGWnj"
