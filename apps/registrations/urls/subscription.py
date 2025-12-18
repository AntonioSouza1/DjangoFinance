from django.urls import path
from apps.registrations.views.subscription import *

app_name = 'subscription'

urlpatterns = [
    path('', SubscriptionsListView.as_view(), name='list'),
    path('create/', SubscriptionCreateView.as_view(), name='create'),
    path('update/<int:pk>', SubscriptionUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', SubscriptionDeleteView.as_view(), name='delete'),
    path('report/', SubscriptionReportView.as_view(), name='report'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>', CategoryDeleteView.as_view(), name='category_delete'),
]
