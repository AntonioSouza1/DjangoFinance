from django.urls import path, include

urlpatterns = [


    #path('supplier/', include('apps.registrations.urls.supplier')),
    #path('bank_account/', include('apps.registrations.urls.bank_account')),
    #path('card/', include('apps.registrations.urls.card')),
    path('user/', include('apps.registrations.urls.user')),
]