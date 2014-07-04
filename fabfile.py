from fabric.api import env, run, task, cd, prefix

env.hosts = ['montrealpython.org']
env.user = 'mtlpyweb'

def deploy(location, name):
	with cd(location):
		run('git pull origin master')
		with prefix('. bin/activate && . env.sh'):
			run('pip install -r requirements.txt')
			run('./manage.py syncdb --migrate')
			run('./manage.py collectstatic --noinput')
			run('sudo /sbin/restart {}'.format(name))

@task
def staging():
	"""Updates the staging server."""
	deploy('/opt/mp/website-stage', 'website-stage')

