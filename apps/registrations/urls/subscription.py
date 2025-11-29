from django.urls import path
from apps.registrations.views.subscription import *

app_name = 'subscription'

urlpatterns = [
    path('', SubscriptionsList.as_view(), name='list'),
    path('create/', SubscriptionCreate.as_view(), name='create'),
    path('update/<int:pk>', SubscriptionUpdate.as_view(), name='update'),
    path('delete/<int:pk>', SubscriptionDelete.as_view(), name='delete'),
    path('report/', SubscriptionReport.as_view(), name='report'),
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/create/', CategoryCreate.as_view(), name='category_create'),
    path('category/update/<int:pk>', CategoryUpdate.as_view(), name='category_update'),
    path('category/delete/<int:pk>', CategoryDelete.as_view(), name='category_delete'),
]
