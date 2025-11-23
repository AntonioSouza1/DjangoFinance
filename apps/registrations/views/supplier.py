from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.registrations.forms.supplier import SupplierForm
from apps.registrations.models.supplier import Supplier
from django.views.generic import ListView
from apps.utils.mixins import *

class SupplierList(LoginRequiredMixin, PermissionRequiredMixin,  SuccessErrorMessageMixin, ListView):
    model = Supplier
    context_object_name = 'suppliers'
    template_name = 'registrations/supplier/list.html'
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'supplier.view_supplier'
    paginate_by = 10

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para acessar a lista de fornecedor.')
            return redirect(reverse_lazy('dashboard:home'))
        return super().handle_no_permission()

    def get_queryset(self):
        f_id = self.request.GET.get('f_id','')
        f_corporate_name = self.request.GET.get('f_corporate_name','')
        f_fantasy_name = self.request.GET.get('f_fantasy_name','')
        f_cpf_cnpj = self.request.GET.get('f_cpf_cnpj','')
        f_status = self.request.GET.get('f_status','')

        filters = {}

        if f_id:
            filters['id'] = f_id
        if f_corporate_name:
            filters['corporate_name__icontains'] = f_corporate_name
        if f_fantasy_name:
            filters['fantasy_name__icontains'] = f_fantasy_name
        if f_cpf_cnpj:
            filters['cpf_cnpj__icontains'] = f_cpf_cnpj
        if f_status:
            filters['status'] = f_status

        suppliers = Supplier.objects.filter(**filters)
        return suppliers

    def get_context_data(self, **kwargs):
        context = super(SupplierList, self).get_context_data(**kwargs)
        context['f_id'] = self.request.GET.get('f_id','')
        context['f_corporate_name'] = self.request.GET.get('f_corporate_name','')
        context['f_fantasy_name'] = self.request.GET.get('f_fantasy_name','')
        context['f_cpf_cnpj'] = self.request.GET.get('f_cpf_cnpj','')
        context['f_situation'] = self.request.GET.get('f_status','')

        return context

class SupplierCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, CreateView):
    model = Supplier
    context_object_name = 'supplier'
    template_name = 'registrations/supplier/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('supplier:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'supplier.add_supplier'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para cadastrar um fornecedor.')
            return redirect(reverse_lazy('supplier:list'))
        return super().handle_no_permission()

class SupplierUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, UpdateView):
    model = Supplier
    context_object_name = 'supplier'
    template_name = 'registrations/supplier/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('supplier:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'supplier.change_supplier'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para editar um fornecedor.')
            return redirect(reverse_lazy('supplier:list'))
        return super().handle_no_permission()


class SupplierDelete(DeleteView):
    success_url = reverse_lazy('supplier:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'supplier.delete_supplier'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para excluir um fornecedor.')
            return redirect(reverse_lazy('supplier:list'))
        return super().handle_no_permission()

    def post(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        try:
            supplier.delete()
            messages.success(request, f"Fornecedor '{supplier}' excluído com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir assinatura: {e}")
        return redirect(self.success_url)
