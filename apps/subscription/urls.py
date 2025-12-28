from django.urls import path
from apps.subscription.views import *

app_name = 'subscription'

urlpatterns = [
    path('', SubscriptionView.as_view(), name='list'),
    path('create/', SubscriptionView.as_view(), name='create'),
    path('update/<int:pk>', SubscriptionView.as_view(), name='update'),
    path('delete/<int:pk>', SubscriptionView.as_view(), name='delete'),
    path('category/', SubscriptionCategoryView.as_view(), name='category_list'),
    path('category/create/', SubscriptionCategoryView.as_view(), name='category_create'),
    path('category/update/<int:pk>', SubscriptionCategoryView.as_view(), name='category_update'),
    path('category/delete/<int:pk>', SubscriptionCategoryView.as_view(), name='category_delete'),
]
