from django.conf import settings
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.models import Permission

#from .models import 

class ProjectPermBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None #skip to next auth backend

    def has_perm(self, user, perm, project = None):
        #We only handle objects of type Project. 
        if project is None or not isinstance(project, Project):
            return False
        
        #Get the latter part of the permission (ie. 'model.can_perm' -> 
        #'can_perm'); then get the 'perm' part.
        try:
            perm = perm.split('.')[-1].split('_')[1]
        except IndexError:
            return False
        
        #Anonymous users have NO permissions for project objects.
        if not user.is_authenticated():
            return False
        
        #MODIFY: Check if user has permission in the project.
        #try:
        #    pp = ProjectPermission.objects.get(user = user, project = project)
        #    #See if user has necessary permissions
        #    pp.permissions.get(codename = 'can_%s' % perm)
        #    return True
        #except (ProjectPermission.DoesNotExist, Permission.DoesNotExist):
        #    return False
        #
        #return False #Shouldn't get here.
