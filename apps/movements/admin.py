from django.contrib import admin
from apps.movements.models.transaction import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description',]

admin.site.register(Transaction, TransactionAdmin)
