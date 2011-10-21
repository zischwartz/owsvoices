from fabric.api import *

from fabric.contrib.console import confirm

env.hosts = ['ec2-user@ec2-107-22-32-186.compute-1.amazonaws.com']

env.path = '/home/ec2-user/conversation/'
env.prj_name = 'voices'
git_repo = 'git://github.com/zischwartz/owsvoices.git'

def prepare_deploy():
    local("./manage.py test posts") #chmod -x manage.py ?
    local("git add . && git commit -m 'commit by fab, prepare_deploy' ")
    local("git push ")

def prepare_server():
	sudo('yum install git-core nginx -y mercurial')
	sudo('easy_install pip')
	sudo('pip install virtualenv')
# pip install supervisor




def first_deploy():
	code_dir = env.path + env.prj_name
	with settings(warn_only=True):
		run('mkdir %s' % env.path)
		with cd(env.path):
			run("git clone %s %s" % (git_repo, code_dir))
			run("virtualenv --no-site-packages . ")
			run("source bin/activate")
			run("pip install -r  %s/requirements.txt" % env.prj_name )

			# run("git clone git@github.com:zischwartz/owsvoices.git %s" % code_dir) 
	# with cd(code_dir):
		# run("git pull")
        # run("touch app.wsgi")


  		# if run("test -d %s" % code_dir).failed:
