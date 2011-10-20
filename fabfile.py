from fabric.api import *

from fabric.contrib.console import confirm

env.hosts = ['ec2-user@ec2-107-22-32-186.compute-1.amazonaws.com/']

env.path = '/home/ec2-user/owsvoices/'

def prepare_deploy():
    local("./manage.py test posts")
    local("git add . && git commit -m 'commit by fab, prepare_deploy' ")

def prepare_server():
	sudo('yum install git-core nginx -y')
	sudo('easy_install pip')
	sudo('pip virtualenv')




def deploy():
    code_dir = env.path
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:zischwartz/owsvoices.git %s" % code_dir) 
    with cd(code_dir):
        run("git pull")
        # run("touch app.wsgi")