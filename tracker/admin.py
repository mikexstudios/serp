from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Track, Check, Profile, PlanFeature

class CheckInline(admin.TabularInline):
    model = Check

class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'local_id', 'user', 'is_active', 'search_engine',
                    'keyword', 'url', 'current_position', 'last_checked')
    list_display_links = ('id', 'keyword')

    inlines = [
        CheckInline,
    ]
    
    def current_position(self, obj):
        #Get the most current position
        c = obj.get_latest_check()
        if c == None:
            #Means that we haven't checked the position yet.
            return 'N/A'
        url = reverse('admin:tracker_check_change', args=[c.id,])
        return '<a href="%s">%s</a>' % (url, c.position)
    current_position.allow_tags = True
admin.site.register(Track, TrackAdmin)

class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'track', 'position', 'pagerank', 'created', 
                    'is_done')
    #list_display_links = ('id',)
    list_filter = ('track',)

    #We don't want the foreign key to be a drop down select. It's too much
    #overhead, so we manually enter in the id of the keyword instead.
    raw_id_fields = ('track',)
admin.site.register(Check, CheckAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'track_increment', )
admin.site.register(Profile, ProfileAdmin)

class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ('plan', 'tracks_max', )
admin.site.register(PlanFeature, PlanFeatureAdmin)
