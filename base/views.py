from django.conf import settings
#import django.contrib.messages as messages
#from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.template import RequestContext
#from django.core.urlresolvers import reverse
#from django.http import HttpResponse
#from django.contrib.auth.decorators import login_required
#from django.contrib.contenttypes.models import ContentType #for adding perm
#from django.contrib.auth.models import Permission #for adding perm

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
#from django.utils.http import urlencode

from annoying.decorators import render_to#, ajax_request
#from annoying.functions import get_object_or_None

#@render_to('base/home.html')
#def home(request):
#
#    return {}
