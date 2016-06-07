from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import mail_admins

#from celery.decorators import task
from celery.task import Task

class SignupNotifyTask(Task):
    '''
    Sends email to admins notifying on each successful new registration.
    '''
    routing_key = 'high'

    def run(self, user_id, **kwargs):
        logger = self.get_logger(**kwargs)

        u = User.objects.get(id = user_id)
        logger.info('Got new user: %s | %s' % (u.id, u.username))

        logger.info('Sending email to admin...')
        mail_admins('New user signup: %s | %s' % (u.id, u.username),
                    '''
A new user has just signed up for SERP app! Brief user info:

ID: %s
Username: %s
Email: %s

SERP app
                    '''.strip() % (u.id, u.username, u.email),
                    fail_silently = True)
        return True
