#!/usr/bin/env python
'''
Automated deployment with fabric.
'''
#from __future__ import with_statement # needed for python 2.5
from fabric.api import *
from fabric.contrib.console import confirm #for yes/no
import os #for environ


###########
# Globals #
###########

#These are fabric built in vars:
env.hosts = ['ssh.supplelabs.com']
env.user = 'serp'
#We don't explicitly set a password here. Instead, you should be using keys to
#authenticate through ssh.
#env.password = '' 

#Our own vars:
env.project_name = 'serp'
env.git_clone_url = 'git@github.com:mikexstudios/serp.git'
#Folder that contains our virtualenv
env.virtualenv_name = 'env'


################
# Environments #
################

def dev():
    '''
    The development environment intended to be an exact setup as the production
    environment. The difference is that we test out new features in the dev
    environment before merging them into prod.
    '''
    #No trailing slashes on paths:
    env.project_path = 'dev/%(project_name)s' % env
    env.git_branch = 'master'

def prod():
    '''
    The environment that actual users will use! Be careful with this!
    '''
    #No trailing slashes on paths:
    env.project_path = 'prod/%(project_name)s' % env
    env.git_branch = 'production'

    confirm('Are you sure you want to use production?')

def admin(user = os.environ['USER']):
    '''
    Sets the user to one with sudo access. By default, we will assume that the
    user has same username as on local machine.

    NOTE: We don't really need to use this since server processes are run under
          non-admin user! Hurrah for unintentional good planning!
    '''
    env.user = user


#########
# Tasks #
#########

def setup():
    '''
    We won't write code for setup because, frankly, this is hardly done. It's just
    safer to setup the server by hand.
    '''
    pass

def restart():
    '''
    Restarts the fcgi server by killing the current process. We rely on daemontools
    to automatically start it again.
    '''
    #We assume that the global variables are set so we don't need to check them.
    #We just check that specific environment vars are set.
    require('project_path')

    with cd(env.project_path):
        #This doesn't work. Probably a paths thing.
        #run('kill `cat fcgi.pid`')
        #So we do it in a more careful manner:
        pid = run('cat fcgi.pid')
        pid = int(pid)
        run('kill %i' % pid)

    print 'Remember to manually restart celery!'

def update():
    '''Updates the git repo.'''
    require('project_path')

    with cd(env.project_path):
        run('git pull')
        #If we updated database schema with South, need to migrate.
        run('source env/bin/activate && ./manage.py migrate')

def ur():
    '''
    Shortcut for updating the git repo followed by restarting the server.
    '''
    update()
    restart()

def reset_env():
    '''
    Deletes existing virutalenv and creates a new one, installing pip and 
    all requirements (excluding local requirements).
    '''
    require('project_path')
    
    confirm('Are you sure you want to reset the env?')

    with cd(env.project_path):
        run('rm -rf env/')
        #This script will take care of setting up new virtualenv, pip, and
        #installs from requirements.txt
        run('./initial_setup.sh')
        #But we also need to install the deploy requirements.
        run('source env/bin/activate && pip -E env install -r deploy/requirements.txt')

def resetdb():
    '''
    For MySQL database only. Drops all tables and then runs syncdb again 
    (fixtures of name initial_data.json are automatically installed).
    '''
    require('project_path')
    
    confirm('Are you sure you want to reset the database?')
    
    with cd(env.project_path):
        run('./helper-scripts/mysql_drop_tables.sh')
        #The problem is that fabric 0.9 doesn't support with prefix(...).
        #So we need to resort to the && hack.
        run('source env/bin/activate && python manage.py syncdb --noinput') #suppress prompts

