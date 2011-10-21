from fabric.api import *

from fabric.contrib.console import confirm
from contextlib import contextmanager as _contextmanager

env.hosts = ['ec2-user@ec2-107-22-32-186.compute-1.amazonaws.com']

env.path = '/home/ec2-user/conversation/'
env.prj_name = 'voices'
env.git_repo = 'git://github.com/zischwartz/owsvoices.git'
env.activate = 'source %sbin/activate' % env.path


def prepare_deploy():
    local("./manage.py test posts") #chmod -x manage.py ?
    local("git add . && git commit -m 'commit by fab, prepare_deploy' ")
    local("git push ")

def prepare_server():
	sudo('yum install git-core nginx -y mercurial python-devel')
	sudo('easy_install pip')
	sudo('pip install virtualenv')
# pip install supervisor

@_contextmanager
def virtualenv():
	with cd(env.path):
		with prefix(env.activate):
			yield


def first_deploy():
	code_dir = env.path + env.prj_name
	with settings(warn_only=True):
		run('mkdir %s' % env.path)
		with cd(env.path):
			run("git clone %s %s" % (env.git_repo, code_dir))
			run("virtualenv --no-site-packages . ")
			with virtualenv():
				run("pip install -r  %s/requirements.txt" % env.prj_name )

			# run("git clone git@github.com:zischwartz/owsvoices.git %s" % code_dir) 
	# with cd(code_dir):
		# run("git pull")
        # run("touch app.wsgi")


  		# if run("test -d %s" % code_dir).failed:
