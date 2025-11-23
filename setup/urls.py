from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dashboard/', include('apps.dashboard.urls')),
    path('registraions/', include('apps.registrations.urls')),
    path('movements/', include('apps.movements.urls')),
    path('reports/', include('apps.reports.urls')),
    path('', include('apps.login.urls')),
    path('admin/', admin.site.urls),
]
