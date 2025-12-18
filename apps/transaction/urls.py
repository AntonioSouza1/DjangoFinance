from django.urls import path
from apps.transaction.views import *

app_name = "transaction"

urlpatterns = [
    #Transações
    path("", TransactionListView.as_view(), name="list"),
    path("create/", TransactionCreateView.as_view(), name="create"),
    path("update/<int:pk>/", TransactionUpdateView.as_view(), name="update"),
    path("detail/<int:pk>/", TransactionDetailView.as_view(), name="detail"),
    path("delete/<int:pk>/", TransactionDeleteView.as_view(), name="delete"),
    path("report/", TransactionReportView.as_view(), name="report"),
    path("pay_off/<int:pk>/", SettleTransactionView.as_view(), name="settle-transaction"),

    #Categorias
    path('category/', TransactionCategoryListView.as_view(), name='category_list'),
    path('category/create/', TransactionCategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>', TransactionCategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>', TransactionCategoryDeleteView.as_view(), name='category_delete'),

    #Grupos
    path('group/', TransactionGroupListView.as_view(), name='group_list'),
    path('group/create/', TransactionGroupCreateView.as_view(), name='group_create'),
    path('group/update/<int:pk>', TransactionGroupUpdateView.as_view(), name='group_update'),
    path('group/delete/<int:pk>', TransactionGroupDeleteView.as_view(), name='group_delete'),

    #Formas de Pagamento
    path('payment/', TransactionPaymentMethodListView.as_view(), name='payment_method_list'),
    path('payment/create/', TransactionPaymentMethodCreateView.as_view(), name='payment_method_create'),
    path('payment/update/<int:pk>', TransactionPaymentMethodUpdateView.as_view(), name='payment_method_update'),
    path('payment/delete/<int:pk>', TransactionPaymentMethodDeleteView.as_view(), name='payment_method_delete'),
]
