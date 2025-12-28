from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import  View
from django.utils import timezone

from apps.transaction.models import Transaction
from apps.subscription.models import Subscription
from apps.utils.mixins import *

today = timezone.now().date()

class Dashboard(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, View):
    login_url = reverse_lazy('login:login')

    def get(self, request, *args, **kwargs):
        try:
            Transaction.objects.filter(
                user=self.request.user,
                status='P',
                due_date__lt=timezone.now().date()  # Filtra transações vencidas
            ).update(status='V')

            subscriptions = Subscription.objects.filter(user=self.request.user, status='A').count()

            total_subscriptions = Subscription.objects.filter(user=self.request.user, status='A').aggregate(total=Sum('value'))['total'] or 0

            transactions_e = Transaction.objects.filter(
                user=self.request.user,
                type='E',
                status='Q',
                payment_date__year=today.year,
                payment_date__month=today.month
            ).count()

            total_transactions_e = Transaction.objects.filter(
                user=self.request.user,
                type='E',
                status='Q',
                payment_date__year=today.year,
                payment_date__month=today.month
            ).aggregate(total=Sum('amount_paid'))['total'] or 0

            transactions_s = Transaction.objects.filter(
                user=self.request.user,
                type='S',
                status='Q',
                payment_date__year=today.year,
                payment_date__month=today.month
            ).count()

            total_transactions_s = Transaction.objects.filter(
                user=self.request.user,
                type='S',
                status='Q',
                payment_date__year=today.year,
                payment_date__month=today.month
            ).aggregate(total=Sum('amount_paid'))['total'] or 0

            transactions_p = Transaction.objects.filter(user=self.request.user, status='P')
            transactions_v = Transaction.objects.filter(user=self.request.user, status='V')

            context = {
                'subscriptions': subscriptions,
                'total_subscriptions': total_subscriptions,
                'transactions_e': transactions_e,
                'transactions_s': transactions_s,
                'total_transactions_e': total_transactions_e,
                'total_transactions_s': total_transactions_s,
                'transactions_p': transactions_p,
                'transactions_v': transactions_v,
            }

            return render(request, 'dashboard/dashboard.html', context)
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao carregar: {e}")
            return render(request, 'dashboard/dashboard.html')
