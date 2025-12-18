from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


def custom_404(request, exception):
    return render(request, 'main/../templates/404.html', status=404)

# Defina o manipulador 404 para a função acima
handler404 = custom_404

urlpatterns = [
    path('dashboard/', include('apps.dashboard.urls')),
    path('registraions/', include('apps.registrations.urls')),
    path('movements/', include('apps.movements.urls')),
    path('', include('apps.login.urls')),
    path('logs/', include('apps.logs.urls')),
    path('admin/', admin.site.urls),
]
