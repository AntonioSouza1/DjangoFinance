from django.urls import path
from apps.logs.views import LogListView

app_name = 'log'

urlpatterns = [
    path('', LogListView.as_view(), name='list'),
]
