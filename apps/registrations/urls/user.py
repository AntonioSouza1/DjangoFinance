from django.urls import path
from apps.registrations.views.user import *

app_name = 'user'

urlpatterns = [
    path('', ListUser.as_view(), name='list'),
    path('create/', UserCreate.as_view(), name='create'),
    path('update/<int:pk>', UserUpdate.as_view(), name='update'),
    path('delete/<int:pk>', UserDelete.as_view(), name='delete'),
    path('<int:pk>/permissions', UserPermissionsUpdate.as_view(), name='permissions_update'),
]