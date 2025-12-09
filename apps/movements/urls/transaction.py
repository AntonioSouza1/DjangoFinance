from django.urls import path
from apps.movements.views.transaction import *

app_name = "transaction"

urlpatterns = [
    path("", TransactionListView.as_view(), name="list"),
    path("create/", TransactionCreateView.as_view(), name="create"),
    path("update/<int:pk>/", TransactionUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", TransactionDeleteView.as_view(), name="delete"),
    path("report/", TransactionReportView.as_view(), name="report"),
    path("pay_off/<int:pk>/", SettleTransactionView.as_view(), name="settle-transaction")
]
