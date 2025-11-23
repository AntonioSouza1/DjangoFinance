from django.urls import path
from apps.registrations.views.supplier import *

app_name = 'supplier'

urlpatterns = [
    path('', SupplierList.as_view(), name='list'),
    path('create/', SupplierCreate.as_view(), name='create'),
    path('update/<int:pk>', SupplierUpdate.as_view(), name='update'),
    path('delete/<int:pk>', SupplierDelete.as_view(), name='delete'),
]