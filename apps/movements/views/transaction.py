from django.contrib.messages.context_processors import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import ContextMixin

from apps.movements.models.transaction import Transaction
from apps.movements.forms.transaction import TransactionForm
from apps.utils.mixins import *

import datetime

date = datetime.date.today()

class TransactionMixin(ContextMixin):

    def get_queryset(self):
        # 1. Pegue os filtros do GET
        f_id = self.request.GET.get('f_id', '')
        f_description = self.request.GET.get('f_description', '')
        f_due_date_of = self.request.GET.get('f_due_date_of', date) #vencimento de
        f_due_date = self.request.GET.get('f_due_date', date) #até
        f_type = self.request.GET.get('f_type', '')
        f_status = self.request.GET.get('f_status', 'T')

        filters = {}

        if f_id:
            filters['id'] = f_id  # <-- Use a variável, não chame o GET de novo
        if f_description:
            filters['description__icontains'] = f_description
        if f_due_date_of:
            filters['due_date__gte'] = f_due_date_of #vencimento de
        if f_due_date:
            filters['due_date__lte'] = f_due_date #até
        if f_status and f_status != 'T':
            filters['status'] = f_status
        if f_type:
            filters['type'] = f_type
        if not filters:
            filters['due_date__year']= date.year
            filters['due_date__month']= date.month
            if not f_status:
                filters['status__in'] = ['P', 'V']

        # 2. Pegue a queryset base da View (importante!)
        #    Isso permite que o Mixin funcione em qualquer ListView
        if hasattr(self, 'model'):
            base_queryset = self.model._default_manager.all()
        else:
            base_queryset = Transaction.objects.all()  # Fallback

        return base_queryset.filter(**filters)

    def get_context_data(self, **kwargs):
        # 1. Bug do super() corrigido
        context = super().get_context_data(**kwargs)

        queryset_filtrada = self.get_queryset()

        total_output_agg = queryset_filtrada.filter(type='S').aggregate(total_output=Sum('amount_paid'))
        total_input_agg = queryset_filtrada.filter(type='E').aggregate(total_input=Sum('amount_paid'))

        # 2. Passe os filtros para o template (para preencher o form)
        context["f_id"] = self.request.GET.get('f_id', '')
        context["f_description"] = self.request.GET.get('f_description', '')
        context["f_due_date_of"] = self.request.GET.get('f_due_date_of', date)
        context["f_due_date"] = self.request.GET.get('f_due_date', date)
        context["f_type"] = self.request.GET.get('f_type', '')
        context["f_status"] = self.request.GET.get('f_status', 'T')
        context["total_output"] = total_output_agg.get('total_output', '')
        context["total_input"] = total_input_agg.get('total_input', '')

        return context

class TransactionListView(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, TransactionMixin, ListView):
    model = Transaction
    template_name = "movements/transaction/list.html"
    context_object_name = "transactions"
    login_url = reverse_lazy('login:login')
    permission_required = 'movements.view_transaction'
    raise_exception = False
    paginate_by = 10

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Você não tem permissão para acessar a lista de transações.")
            return redirect(reverse_lazy('dashboard:home'))
        return super().handle_no_permission()


class TransactionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "movements/transaction/form.html"
    success_url = reverse_lazy("transaction:list")
    permission_required = 'movements.add_transaction'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Você não tem permissão criar uma nova transação.")
            return redirect(reverse_lazy('transaction:list'))
        return super().handle_no_permission()


class TransactionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "movements/transaction/form.html"
    success_url = reverse_lazy("transaction:list")
    permission_required = 'movements.change_transaction'
    raise_exception = False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Você não tem permissão editer uma nova transição.")
            return redirect(reverse_lazy('transaction:list'))
        return super().handle_no_permission()

class TransactionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, DeleteView):
    success_url = reverse_lazy('transaction:list')
    login_url = reverse_lazy('login:login')
    permission_required = 'movements.delete_transaction'
    raise_exception = False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Você não tem permissão para excluir uma transação.")
            return redirect(reverse_lazy('transaction:list'))
        return super().handle_no_permission()

    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        try:
            if transaction.status != 'Q':
                transaction.delete()
                messages.success(request, f"Transação '{transaction}' excluída com sucesso.")
            else:
                messages.error(request, 'Não e possivel excluir transações já quitadas')
        except Exception as e:
            messages.error(request, f"Erro ao excluir transação: {e}")
        return redirect(self.success_url)

class TransactionReportView(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, TransactionMixin, ListView):
    model = Transaction
    template_name = "movements/transaction/report.html"
    context_object_name = "transactions"
    login_url = reverse_lazy('login:login')
    permission_required = 'movements.view_transaction'
    raise_exception = False
