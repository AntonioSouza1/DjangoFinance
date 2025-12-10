from django.contrib.messages.context_processors import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.dateparse import parse_date
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import ContextMixin

from apps.movements.models.transaction import Transaction
from apps.movements.forms.transaction import TransactionForm
from apps.utils.mixins import *

import datetime
from django.utils import timezone

date = datetime.date.today()

from django.views.generic.base import ContextMixin
from django.db.models import Sum
from datetime import date


class TransactionListMixin(ContextMixin):
    """
    Mixin para filtrar transações por usuário (Multi-tenancy) e filtros de busca.
    Deve ser usado em conjunto com ListView.
    """

    # NÃO use __init__ em Mixins de View para setar self.request.
    # O Django injeta o request automaticamente antes de chamar get_queryset.

    def get_queryset(self):
        # 1. Pega a QuerySet base da View principal (ex: Transaction.objects.all())
        # Isso é vital para o Mixin funcionar com qualquer Model
        queryset = super().get_queryset()

        # 2. APLICA O MULTI-TENANCY (Segurança Primeiro)
        # Garante que o usuário só veja os dados dele antes de qualquer filtro
        queryset = queryset.filter(user=self.request.user)

        # 3. Captura os parâmetros do GET
        data = self.request.GET

        # Define defaults apenas se necessário
        f_id = data.get('f_id')
        f_description = data.get('f_description')
        f_due_date_of = data.get('f_due_date_of')
        f_due_date = data.get('f_due_date')
        f_type = data.get('f_type')
        f_status = data.get('f_status', 'T')

        filters = {}

        if f_id:
            filters['id'] = f_id
        if f_description:
            filters['description__icontains'] = f_description
        if f_due_date_of:
            filters['due_date__gte'] = f_due_date_of
        if f_due_date:
            filters['due_date__lte'] = f_due_date
        if f_status and f_status != 'T':
            filters['status'] = f_status
        if f_type:
            filters['type'] = f_type

        # Lógica de Default: Se não tem filtros explícitos, mostra o mês atual
        # Nota: verifique se isso não conflita com a navegação do usuário
        has_filters = any([f_id, f_description, f_due_date_of, f_due_date, f_type, (f_status != 'T')])

        if not has_filters:
            today = date.today()
            filters['due_date__year'] = today.year
            filters['due_date__month'] = today.month
            # Se não tem status definido, pega pendentes e vencidos?
            # filters['status__in'] = ['P', 'V']

        return queryset.filter(user=self.request.user, **filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Reutiliza a queryset já filtrada pelo método acima
        queryset_filtrada = self.get_queryset()  # Agora é um método, usa ()

        # Agregações
        # Dica: Use (Result or 0) para evitar que retorne "None" se não houver dados
        total_output = queryset_filtrada.filter(type='S').aggregate(s=Sum('amount_paid'))['s'] or 0
        total_input = queryset_filtrada.filter(type='E').aggregate(s=Sum('amount_paid'))['s'] or 0

        # Atualiza o contexto com os totais
        context["total_output"] = total_output
        context["total_input"] = total_input
        context["saldo"] = total_input - total_output  # Opcional: já manda o saldo

        # Retorna os filtros para manter o formulário preenchido no template
        # Dica: passar request.GET direto economiza linhas
        context.update(self.request.GET.dict())

        # Garante defaults no contexto se não vieram no GET
        if 'f_status' not in context: context['f_status'] = 'T'

        return context

class TransactionListView(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, TransactionListMixin, ListView):
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


class TransactionCreateView(LoginRequiredMixin, PermissionRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, CreateView):
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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, PermissionRequiredMixin,  UserIsOwnerMixin, SuccessErrorMessageMixin, UpdateView):
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

class TransactionReportView(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, TransactionListMixin, ListView):
    model = Transaction
    template_name = "movements/transaction/report.html"
    context_object_name = "transactions"
    login_url = reverse_lazy('login:login')
    permission_required = 'movements.view_transaction'
    raise_exception = False


class SettleTransactionView(View, SuccessErrorMessageMixin):
    def post(self, request, pk):

        transaction = get_object_or_404(Transaction, pk=pk)

        try:
            if transaction.status == 'Q':
                messages.error(request, 'Transação já baixada')
            else:
                date = parse_date(request.POST.get('date'))
                if date:
                    if date < timezone.now().date():
                        transaction.status = 'Q'
                        transaction.payment_date = self.request.POST['date']
                        transaction.save()
                        messages.success(request, 'Transação baixada com sucesso')
                    else:
                        messages.error(request, 'A data informada e maior que a data atual')
                else:
                    transaction.status = 'Q'
                    transaction.payment_date = timezone.now().date()
                    transaction.save()
                    messages.success(request, f'Transação baixada com sucesso usando a data: {transaction.payment_date}')

        except Exception as e:
            messages.error(request, 'Erro ao baixar transação')

        return redirect(reverse_lazy('transaction:list'))
