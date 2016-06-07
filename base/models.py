from django.db import models

import django_rpx_plus.signals as drp_signals

from .tasks import SignupNotifyTask

# Create your models here.

# We also put our signal handlers here.
def handle_registration_successful(sender, **kwargs):
    user = kwargs['user']

    #We queue sending an email to admin telling us about the new signup!
    SignupNotifyTask.delay(user.id)
drp_signals.registration_successful.connect(handle_registration_successful)
