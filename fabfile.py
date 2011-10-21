from fabric.api import *

from fabric.contrib.console import confirm
from contextlib import contextmanager as _contextmanager

env.hosts = ['ec2-user@ec2-107-22-54-148.compute-1.amazonaws.com']

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
	#for mongodb
	sudo('yum -y install git tcsh scons gcc-c++ glibc-devel')
	sudo('yum -y install boost-devel pcre-devel js-devel readline-devel')
	sudo('yum -y install boost-devel-static readline-static ncurses-staticl')
	sudo('easy_install pip')
	sudo('pip install virtualenv')

	#for 32 bit
	sudo('yum install http://downloads-distro.mongodb.org/repo/redhat/os/i686/RPMS/mongo-10gen-2.0.0-mongodb_1.i686.rpm -y --nogpgcheck')
	sudo('yum install http://downloads-distro.mongodb.org/repo/redhat/os/i686/RPMS/mongo-10gen-server-2.0.0-mongodb_1.i686.rpm -y --nogpgcheck')
	#64 bit at http://downloads-distro.mongodb.org/repo/redhat/os/

	sudo('mkdir -p /data/db/')
	sudo('sudo chown `id -u` /data/db')



# pip install supervisor, guicorn
# http://senko.net/en/django-nginx-gunicorn/
#http://gunicorn.org/run.html#gunicorn-django

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
