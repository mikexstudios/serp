from django.contrib import admin
#from django.core.urlresolvers import reverse

from .models import Plan, Subscription

class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'recurring_period', 'recurring_unit',)
    list_display_links = ('id', 'name')
admin.site.register(Plan, PlanAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'expires', 'is_cancelled', 'created')
    list_display_links = ('id', )
admin.site.register(Subscription, SubscriptionAdmin)

