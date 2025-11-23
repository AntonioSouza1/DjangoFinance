from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from apps.utils.mixins import *
from apps.registrations.forms.bank_account import *
from apps.registrations.models.bank_account import *


class BankAccountList(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, ListView):
    model = BankAccount
    context_object_name = 'bank_accounts'
    template_name = 'registrations/bank_account/list.html'
    paginate_by = 10
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'registrations.view_bankaccount'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para acessar a lista de contas bancarias.')
            return redirect(reverse_lazy('dashboard:home'))
        return super().handle_no_permission()

    def get_queryset(self):
        f_id = self.request.GET.get('f_id', '')
        f_bank = self.request.GET.get('f_bank', '')
        f_type = self.request.GET.get('f_type', '')
        f_status = self.request.GET.get('f_status', '')

        filters = {}

        if f_id:
            filters['bank_accounts'] = f_id
        if f_bank:
            filters['bank_name__icontains'] = f_bank
        if f_type:
            filters['account_type'] = f_type
        if f_status:
            filters['status'] = f_status

        banks = BankAccount.objects.filter(**filters)

        return banks

    def get_context_data(self, **kwargs):
        context = super(BankAccountList, self).get_context_data(**kwargs)
        context['filter_id'] = self.request.GET.get('f_id', '')
        context['filter_bank'] = self.request.GET.get('f_bank', '')
        context['filter_type'] = self.request.GET.get('f_type', '')
        context['f_status'] = self.request.GET.get('f_status', '')
        return context

class BankAccountCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, CreateView):
    model = BankAccount
    context_object_name = 'bank_account'
    template_name = 'registrations/bank_account/form.html'
    form_class = BankAccountForm
    success_url = reverse_lazy('bank_account:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'registrations.add_bankaccount'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para cadastrar uma conta bancaria.')
            return redirect(reverse_lazy('bank_account:list'))
        return super().handle_no_permission()

class BankAccountUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, UpdateView):
    model = BankAccount
    context_object_name = 'bank_account'
    template_name = 'registrations/bank_account/form.html'
    form_class = BankAccountForm
    success_url = reverse_lazy('bank_account:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'registrations.change_bankaccount'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para editar uma conta bancaria.')
            return redirect(reverse_lazy('bank_account:list'))
        return super().handle_no_permission()

class BankAccountDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    success_url = reverse_lazy('bank_account:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'registrations.delete_bankaccount'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para excluir uma conta bancaria.')
            return redirect(reverse_lazy('bank_account:list'))
        return super().handle_no_permission()

    def post(self, request, pk):
        bank = get_object_or_404(BankAccount, pk=pk)
        try:
            bank.delete()
            messages.success(request, f"Banco '{bank}' excluída com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir banco: {e}")
        return redirect(self.success_url)
