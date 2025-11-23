from django.urls import path
from apps.login import views

app_name = 'login'

urlpatterns = [
    path('', views.login_form, name='login'),
    path('logout/', views.logout_form, name='logout'),
]