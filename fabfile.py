from fabric.api import local

def prepare_deploy():
    local("./manage.py test posts")
    local("git add . && git commit -m 'commit by fab, prepare_deploy' ")