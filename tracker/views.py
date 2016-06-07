from django.conf import settings
import django.contrib.messages as messages
from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.contrib.contenttypes.models import ContentType #for adding perm
#from django.contrib.auth.models import Permission #for adding perm

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
#from django.utils.http import urlencode

from annoying.decorators import render_to, ajax_request
#from annoying.functions import get_object_or_None

from .forms import AddURLForm, RefreshForm, ActionsForm
from .models import Track, Check
#from .tasks import InstantCheckRankingTask

import gviz_api #to implement Google Visualization datasource
import datetime

@login_required
@render_to('tracker/dashboard.html')
def dashboard(request):
    #Get list of tracker items.
    t = Track.objects.filter(user = request.user, is_active = True).order_by('id')

    return {'tracks': t}

@login_required
@render_to('tracker/archived.html')
def archived(request):
    #Get list of tracker items.
    t = Track.objects.filter(user = request.user, is_active = False).order_by('id')

    return {'tracks': t}

def _actions(request):
    '''
    Private method to that contains common code for dashboard and archived actions.
    '''
    if request.method == 'POST':
        form = ActionsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #print data
            #NOTE: Our form validation guarantees that we'll have len(ids) > 0.
            
            if data['action'] == 'refresh':
                for id in data['id']:
                    try:
                        #Get only active Tracks for refresh.
                        t = Track.objects.get(local_id = id, is_active = True, user = request.user)
                        t.refresh(time_between_refresh = settings.TIME_BETWEEN_REFRESH,
                                  ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1'))
                    except Track.DoesNotExist:
                        pass #do nothing
                messages.success(request, 'Selected track IDs that can be refreshed are being refreshed...')
            elif data['action'] == 'archive':
                for id in data['id']:
                    try:
                        t = Track.objects.get(local_id = id, user = request.user)
                        t.is_active = False
                        t.save()
                    except Track.DoesNotExist:
                        pass #do nothing
                messages.success(request, 'Selected track IDs were successfully archived.')
            elif data['action'] == 'unarchive':
                for id in data['id']:
                    try:
                        t = Track.objects.get(local_id = id, user = request.user)
                        t.is_active = True
                        t.save()
                    except Track.DoesNotExist:
                        pass #do nothing
                messages.success(request, 'Selected track IDs were successfully unarchived.')
            elif data['action'] == 'delete':
                for id in data['id']:
                    try:
                        t = Track.objects.get(local_id = id, user = request.user)
                        t.delete()
                    except Track.DoesNotExist:
                        pass #do nothing
                messages.success(request, 'Selected track IDs were successfully deleted.')
        else:
            #Put our error messages in messages.error
            for field, errors in form.errors.items():
                #There may be multiple errors per field.
                for error in errors:
                    messages.error(request, error)

@login_required
def dashboard_actions(request):
    _actions(request)
    return redirect('dashboard')

@login_required
def archived_actions(request):
    _actions(request)
    return redirect('archived')

@login_required
@render_to('tracker/add.html')
def add(request):
    #See if user has reached limits of plan
    user_num_tracks = Track.get_num_active_for_user(request.user)
    planfeature = request.user.subscription.plan.planfeature
    num_tracks_max = planfeature.tracks_max
    percent_used = float(user_num_tracks)/float(num_tracks_max) * 100.0
    if user_num_tracks >= num_tracks_max:
        return {'is_reached_limit': True, 'user_num_tracks': user_num_tracks,
                'num_tracks_max': num_tracks_max, 'percent_used': percent_used, }

    if request.method == 'POST':
        form = AddURLForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #print data

            t = Track()
            t.user = request.user
            t.keyword = data['keyword']
            t.url = data['url'] #wildcard enabled
            t.save()

            messages.success(request, 'New URL successfully added. Please wait, getting initial ranking data now...')
            
            #Redirect to URL's history page so that it will be refreshed immediately.
            return redirect('history', t.local_id)
    else: 
        form = AddURLForm()
    
    return {'form': form, 'user_num_tracks': user_num_tracks,
            'num_tracks_max': num_tracks_max, 'percent_used': percent_used, }

@login_required
@render_to('tracker/history.html')
def history(request, track_id):
    t = get_object_or_404(Track, user = request.user, local_id = track_id)
    
    #Return latest 99 checks. 99 since div by 3.
    checks = t.check_set.filter(is_done = True).order_by('-created')[:99]

    #Count how many records we have. Then split into three parts such that
    #each of the three parts has about equal elements.
    total_checks = checks.count()
    if total_checks >= 3:
        num_each_part = total_checks / 3
        overflow = total_checks % 3
        #Handle overflow by distributing it evenly across three columns. If we have
        #two extra entries, then place in columns 1 and 2. If only one entry, place
        #in column 3.
        if overflow >= 2:
            #The offset tells the template where to restart the count for each
            #new table. 
            offsets = [0, num_each_part + 1,]
            offsets.append(offsets[1] + num_each_part + 1)
        else:
            offsets = [0, num_each_part,]
            offsets.append(offsets[1] + num_each_part)

        #Now slice checks into three columns
        #We need to pass offset since template filters/tags aren't smart enough.
        checks_parts = []
        checks_parts.append( (offsets[0], 
                              checks[:offsets[1]]) )
        checks_parts.append( (offsets[1], 
                              checks[offsets[1]:offsets[2]]) )
        checks_parts.append( (offsets[2], 
                              checks[offsets[2]:]) )
    elif total_checks <= 0:
        #This is a completely new entry, so we don't want to return a list; this
        #allows us to use {% empty %} in the for loop.
        checks_parts = None
    else:
        #So we have <= 2 entries.
        checks_parts = [ (0,
                          checks[:1]) ]
        checks_parts.append( (1, checks[1:]) )
        checks_parts.append( (0, None) )

    #Also, determine if we should show the refresh link.
    is_refresh_interval = True
    now = datetime.datetime.now()
    if t.last_checked + settings.TIME_BETWEEN_REFRESH > now:
        is_refresh_interval = False
    
    return {'track': t, 'checks_parts': checks_parts, 
            'is_refresh_interval': is_refresh_interval}
            

@login_required
def history_datasource(request, track_id):
    t = get_object_or_404(Track, user = request.user, local_id = track_id)
    
    description = {'created': ('datetime', 'Date Checked'),
                   'position': ('number', 'Ranking Position'),}

    data_table = gviz_api.DataTable(description)

    #Now add our data. checks is a list of dictionaries.
    checks = t.check_set.filter(is_done = True).values('created', 'position')
    #Make the positions negative. Could we do this in a better way? Also,
    #if position is None, we'll make it our maximum limit so that we still have
    #a data point.
    for c in checks:
        if c['position'] == None:
            c['position'] = settings.MAX_SEARCH_RESULTS
        c['position'] *= -1
    data_table.AppendData(checks)
    
    #tqx contains custom paramaters/configs. ToResponse parses the 'out' part
    #of tqx, which states what format is requested for return.
    tqx = request.GET.get('tqx', '')
    return HttpResponse(data_table.ToResponse(tqx = tqx))

@login_required
@ajax_request
def refresh(request, track_id):
    t = get_object_or_404(Track, user = request.user, local_id = track_id)

    if request.method == 'POST':
        form = RefreshForm(request.POST)
        if form.is_valid():
            #data = form.cleaned_data
            #print data
            
            #The refresh method returns a dictionary that we can pass back as
            #JSON result.
            return t.refresh(time_between_refresh = settings.TIME_BETWEEN_REFRESH,
                             ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1'))

    #Means that user accessed url directly or form failed.
    return {'success': False}

@login_required
@ajax_request
def refresh_poll(request, track_id):
    t = get_object_or_404(Track, user = request.user, local_id = track_id)

    #Get checks associated with the Track that have not been completed.
    checks = t.check_set.filter(is_done = False)

    total_count = checks.count()
    #If we don't have any checks in progress, then we are done.
    if total_count <= 0:
        return {'all_done': True}

    #Otherwise, we still have checks running. 
    return {'all_done': False, 'total': total_count}

