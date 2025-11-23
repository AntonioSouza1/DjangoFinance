from django.urls import path
from apps.reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.Reports.as_view(), name='home'),
]