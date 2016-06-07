from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from annoying.fields import AutoOneToOneField
#Need to tell south that this field is okay:
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^annoying\.fields\.AutoOneToOneField"])

from datetime import datetime

class Check(models.Model):
    #id is auto-defined and is auto-incrementing
    track = models.ForeignKey('Track')
    #If position is null, that means not found.
    position = models.PositiveIntegerField(null = True, blank = True)
    pagerank = models.PositiveSmallIntegerField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    is_done = models.BooleanField(default = False)
    
    def __unicode__(self):
        return '%s. %s' % (self.id, self.position)

    def change_from_previous_position(self):
        try:
            #We have the created__lt case since we don't want to select ourself.
            prev = Check.objects.filter(track = self.track, created__lt = self.created).order_by('-created')[0]
        except IndexError:
            #We don't have any previous case.
            return 0

        #print '%s | %s' % (self.position, prev.position)

        #If we don't have any change, return 0
        if self.position == prev.position:
            return 0

        #If we don't have a current position, means we dropped from the prev 
        #position.
        if not self.position and prev.position:
            #Maybe return '+'?
            return 'down'
        #If we don't have prev position, but we have current pos. Means we just
        #appeared on the map. Show arrow but no number.
        elif self.position and not prev.position:
            return 'up'
        #Otherwise, we have two integers that we can subtract. Note the order
        #of subtraction.
        return prev.position - self.position


SEARCH_ENGINE_CHOICES = (
    ('google', 'Google'),
)
URL_MATCH_TYPE = (
    ('exact', 'Exact URL'),
    ('domain', 'Entire Domain')
)
class Track(models.Model):
    #id is auto-defined and is auto-incrementing
    #local_id is not autoincrementing, but we fake that in save().
    local_id = models.IntegerField(db_index = True, blank = True, editable = False)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default = True) #False implies archived
    search_engine = models.CharField(max_length = 20, default = 'google', choices = SEARCH_ENGINE_CHOICES)
    keyword = models.CharField(max_length = 250)
    #Instead of using URLField, we allow some wildcard characters in url so we need
    #to use a CharField instead.
    url = models.CharField(max_length = 1000)
    #Contains the datetime of the latest check. We add this for convenience in
    #selecting things. We set default value to the earliest time we can get so that
    #our .filter(...) criteria can pick it up.
    last_checked = models.DateTimeField(default = datetime.min)
    created = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return '%s. %s | %s' % (self.id, self.keyword, self.url)

    def save(self, *args, **kwargs):
        '''
        We want to have the local_id automatically set before save.
        '''
        #Only set local_id for new objects.
        if self.local_id == None:
            self.local_id = self.user.profile.get_next_track_id()
        super(Track, self).save(*args, **kwargs)

    def latest_check(self):
        '''
        Returns the most recent completed Check object associated with Track.
        '''
        try:
            return self.check_set.filter(is_done = True).order_by('-created')[0]
        except IndexError:
            return None

    def check_set_done(self):
        '''
        Like check_set, but filters checks that are done.
        '''
        return self.check_set.filter(is_done = True)

    def checks_order_by_created_desc(self):
        return self.check_set.all().order_by('-created')
    
    @staticmethod
    def get_num_active_for_user(user):
        return Track.objects.filter(user = user, is_active = True).count()

    def refresh(self, time_between_refresh = None, ip_address = '127.0.0.1'):
        '''
        Creates a new Check.
        '''
        #Make sure there isn't already a check task running for this Track.
        #TODO: When we have multiple search engines, we need to expand our
        #      checking for existing task.
        existing_checks = self.check_set.filter(is_done = False)
        if existing_checks.count() > 0:
            #Check to see if the time interval for the task that is
            #running is too long that we need to expire it.
            now = datetime.now()
            any_task_revoked = False #flag for determining if we revoked any task
            for c in existing_checks:
                if c.created + settings.FROZEN_CHECK_EXPIRE_TIME <= now:
                    #This will also delete the check object.
                    #There is no way, right now, to delete a task while it
                    #is running. So we just delete the record.
                    c.delete()
                    any_task_revoked = True
            
            #TODO: shouldn't this be without the 'not'?!!
            if not any_task_revoked: #no tasks revoked
                #We send back success since this will allow our spinners to activate.
                return {'success': True}

        #Check to see when was the last time we refreshed. If less than 
        #settings.TIME_BETWEEN_REFRESH, then we won't allow it to happen.
        now = datetime.now()
        if time_between_refresh and self.last_checked + time_between_refresh > now:
            #Means that not enough time has passed.
            refresh_interval = time_between_refresh.seconds / 3600
            return {'success': False, 
                    'error': 'Please wait %s hours between refreshes.' % refresh_interval}

        #Create a new task for checking search result. Since we are checking
        #immediately and since the Check may not necessarily immediately
        #execute, we create a Check object first as a placeholder.
        #TODO: Put in high priority queue.
        c = Check()
        c.track = self
        c.save()
        result = InstantCheckRankingTask.apply_async(args = [self.id, c.id, ip_address],
                                                     routing_key = 'high')
        return {'success': True}


class Profile(models.Model):
    '''
    Extended fields for User Profile.
    '''
    user = AutoOneToOneField(User, primary_key = True)
    #Keeps track of what is the next track number.
    track_increment = models.PositiveIntegerField(default = 1)

    def get_next_track_id(self):
        next_id = self.track_increment
        self.track_increment += 1
        self.save()
        return next_id

class PlanFeature(models.Model):
    '''
    Contains limitations/attributes of the plan.
    '''
    plan = models.OneToOneField('subscription.Plan', primary_key = True)
    tracks_max = models.PositiveIntegerField()
    #TODO: Add pagerank flag, incoming links, different search engines.


#Resolve circular import issues
from .tasks import InstantCheckRankingTask
