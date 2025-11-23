from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import  View
import datetime

from apps.movements.models.transaction import Transaction
from apps.registrations.models.subscription import Subscription

today = datetime.date.today()

class Dashboard(LoginRequiredMixin, View):
    login_url = reverse_lazy('login:login')
    def get(self, request, *args, **kwargs):
        subscriptions = Subscription.objects.filter(status='A').count()
        total_subscriptions = Subscription.objects.filter(status='A').aggregate(total=Sum('value'))['total'] or 0

        transactions_e = Transaction.objects.filter(
            type='E',
            status='Q',
            payment_date__year=today.year,
            payment_date__month=today.month
        ).count()

        total_transactions_e = Transaction.objects.filter(
            type='E',
            status='Q',
            payment_date__year=today.year,
            payment_date__month=today.month
        ).aggregate(total=Sum('value'))['total'] or 0

        transactions_s = Transaction.objects.filter(
            type='S',
            status='Q',
            payment_date__year=today.year,
            payment_date__month=today.month
        ).count()

        total_transactions_s = Transaction.objects.filter(
            type='S',
            status='Q',
            payment_date__year=today.year,
            payment_date__month=today.month
        ).aggregate(total=Sum('value'))['total'] or 0

        context = {
            'subscriptions': subscriptions,
            'total_subscriptions': total_subscriptions,
            'transactions_e': transactions_e,
            'transactions_s': transactions_s,
            'total_transactions_e': total_transactions_e,
            'total_transactions_s': total_transactions_s,
        }

        return render(request, 'dashboard.html', context)
