"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ

bind = '127.0.0.1:' + environ['GUNICORN_PORT']
max_requests = 1000
worker_class = 'sync'
workers = cpu_count() * 2 + 1

proc_name = 'website-prod'

errorlog = 'log/error.log'
accesslog = 'log/access.log'

tmp_upload_dir = 'tmp'

user = 'nobody'
group = 'www-data'

