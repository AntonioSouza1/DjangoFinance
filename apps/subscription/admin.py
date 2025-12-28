from django.contrib import admin
from apps.subscription.models import *

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user','description','category', 'value', 'status']
    list_filter = ['user', 'status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'name',]

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Category, CategoryAdmin)
