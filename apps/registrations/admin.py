from django.contrib import admin
from apps.registrations.models.subscription import *
from apps.registrations.models.supplier import *
from apps.registrations.models.card import *
from apps.registrations.models.bank_account import *

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user','description','category', 'value', 'status']
    list_filter = ['user', 'status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category',]

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Category, CategoryAdmin)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['corporate_name']

admin.site.register(Supplier, SupplierAdmin)

class CardAdmin(admin.ModelAdmin):
    list_display =  ['card_name']

admin.site.register(Card, CardAdmin)

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['bank_name']

admin.site.register(BankAccount, BankAccountAdmin)