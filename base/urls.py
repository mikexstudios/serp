from django.conf.urls.defaults import *
#from django.conf import settings

#from .models import 

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'base/home.html'}, name='home'), #default url
    url(r'^signup/$', 'direct_to_template', {'template': 'base/signup.html'}, name='signup'),
)

#urlpatterns = patterns('base.views',
#    url(r'^$', 'home', name='home'), #default url
#)

#urlpatterns += patterns('',
#    url(r'^example/$', 'django.views.generic.simple.redirect_to', 
#                        {'url': '/', 'permanent': False}),
#)
