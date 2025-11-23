from django.urls import include, path

urlpatterns = [
    path('transaction/', include('apps.movements.urls.transaction')),
]