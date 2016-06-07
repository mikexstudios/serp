from django.conf.urls.defaults import *
from django.conf import settings #for MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^', include('base.urls')),
    (r'^', include('tracker.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admineral/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admineral/', include(admin.site.urls)),
    
    #URLs for django-rpx-plus:                   
    #url(r'^accounts/$', 'django.views.generic.simple.redirect_to', 
    #                    {'url': '/accounts/profile/', 'permanent': False},
    #                    name='auth_home'),
    #url(r'^accounts/profile/$', 'tracker.views.edit_user_profile', name='edit_profile'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
                      {'template_name': 'django_rpx_plus/logged_out.html'}, 
                      name='auth_logout'),
    #url(r'^accounts/associate/delete/(\d+)/$', tracker.views.delete_associated_login, name='delete-associated-login'),
    (r'^accounts/', include('django_rpx_plus.urls')),

    #Temporary fix for serving static files in dev environment.
    #See: http://docs.djangoproject.com/en/dev/howto/static-files/
    #In production setting, the webserver automatically overrides this, 
    #so there is no need to take this out when in production:
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
)
