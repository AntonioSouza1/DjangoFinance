from django.urls import path
from apps.registrations.views.card import *

app_name = 'card'

urlpatterns = [
    path('', CardList.as_view(), name='list'),
    path('create/', CardCreate.as_view(), name='create'),
    path('update/<int:pk>', CardUpdate.as_view(), name='update'),
    path('delete/<int:pk>', CardDelete.as_view(), name='delete'),
]
