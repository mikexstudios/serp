from django.conf.urls.defaults import *
#from django.conf import settings

#from .models import 

urlpatterns = patterns('tracker.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^dashboard/actions/$', 'dashboard_actions', name='dashboard_actions'),
    url(r'^archived/$', 'archived', name='archived'),
    url(r'^archived/actions/$', 'archived_actions', name='archived_actions'),
    url(r'^add/$', 'add', name='add'),
    url(r'^refresh/(\d+)/$', 'refresh', name='refresh'),
    url(r'^refresh/(\d+)/poll/$', 'refresh_poll', name='refresh_poll'),
    url(r'^view/(\d+)/$', 'history', name='history'),
    url(r'^view/(\d+)/data/$', 'history_datasource', name='history_data'),
)

#urlpatterns += patterns('',
#    url(r'^example/$', 'django.views.generic.simple.redirect_to', 
#                        {'url': '/', 'permanent': False}),
#)
