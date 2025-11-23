from django.urls import path
from apps.registrations.views.bank_account import *

app_name = 'bank_account'

urlpatterns = [
    path('', BankAccountList.as_view(), name='list'),
    path('create/', BankAccountCreate.as_view(), name='create'),
    path('update/<int:pk>', BankAccountUpdate.as_view(), name='update'),
    path('delete/<int:pk>', BankAccountDelete.as_view(), name='delete'),
]
