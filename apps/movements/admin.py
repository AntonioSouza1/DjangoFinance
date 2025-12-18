from django.contrib import admin
from apps.movements.models.transaction import Transaction, TransactionCategory, TransactionGroup, TransactionPaymentMethod

class TransactionPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'name',]
    list_filter = ['user',]
    list_display_links = ['name', ]
    search_fields = ['name', 'user__name',]
    list_per_page = 50

class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'name',]
    list_filter = ['user',]
    list_display_links = ['name', ]
    search_fields = ['name', 'user__name',]
    list_per_page = 50

class TransactionGroupAdmin(admin.ModelAdmin):
    list_display = ['user', 'name',]
    list_filter = ['user',]
    list_display_links = ['name', ]
    search_fields = ['name', 'user__name',]
    list_per_page = 50

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'description', 'amount_paid', 'due_date', 'payment_date', 'status']
    list_filter = ['user', 'type']
    list_display_links = ['description', ]
    search_fields = ['description', 'subscription__description']
    list_per_page = 50

admin.site.register(TransactionCategory, TransactionCategoryAdmin)
admin.site.register(TransactionGroup, TransactionGroupAdmin)
admin.site.register(TransactionPaymentMethod, TransactionPaymentMethodAdmin)
admin.site.register(Transaction, TransactionAdmin)
