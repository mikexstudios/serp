from django.db import models
from django.contrib.auth.models import User

from annoying.fields import AutoOneToOneField
#Need to tell south that this field is okay:
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^annoying\.fields\.AutoOneToOneField"])

#from datetime import datetime

TIME_UNIT_CHOICES = (
    ('D', 'Day'),
    ('W', 'Week'),
    ('M', 'Month'),
    ('Y', 'Year'),
)
class Plan(models.Model):
    '''
    Describes a subscription plan.
    '''
    name = models.CharField(unique = True, max_length = 100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default='0')
    
    #If a period is set, means that we have a recurring charge.
    recurring_period = models.PositiveIntegerField(null = True, blank = True)
    recurring_unit = models.CharField(null = True, blank = True, max_length = 1, 
                                      choices = TIME_UNIT_CHOICES)
    #TODO: Fields for trial

    def __unicode__(self):
        return self.name

class Subscription(models.Model):
    '''
    Maps User to a Plan.
    '''
    user = AutoOneToOneField(User)
    #We have the first Plan be the default plan. This will typically be the 
    #"free" plan.
    plan = models.ForeignKey(Plan, default = 1)
    
    #If expires is NULL, then we assume that it never expires (ie. lifetime acct).
    expires = models.DateTimeField(null = True, blank = True)
    #If user cancels subscription before expiration, we will mark it as cancelled
    #but keep it active until the expiration date.
    is_cancelled = models.BooleanField(default = False)
    
    created = models.DateTimeField(auto_now_add = True)
