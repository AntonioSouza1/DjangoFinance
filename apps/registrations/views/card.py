from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from apps.utils.mixins import *
from apps.registrations.forms.card import *
from apps.registrations.models.card import *


class CardList(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, ListView):
    model = Card
    context_object_name = 'cards'
    paginate_by = 10
    template_name = 'registrations/card/list.html'
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'registrations.view_card'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para acessar a lista de cartões.')
            return redirect(reverse_lazy('dashboard:home'))
        return super().handle_no_permission()

    def get_queryset(self):
        f_id = self.request.GET.get('f_id', '')
        f_card = self.request.GET.get('f_card', '')
        f_type = self.request.GET.get('f_type', '')
        f_status = self.request.GET.get('f_status', '')

        filters = {}

        if f_id:
            filters['id'] = f_id
        if f_card:
            filters['card_name__icontains'] = f_card
        if f_type:
            filters['card_type'] = f_type
        if f_status:
            filters['status'] = f_status

        cards = Card.objects.filter(**filters)

        return cards

    def get_context_data(self, **kwargs):
        context = super(CardList, self).get_context_data(**kwargs)
        context['f_id'] = self.request.GET.get('f_status', '')
        context['f_card'] = self.request.GET.get('f_card', '')
        context['f_type'] = self.request.GET.get('f_type', '')
        context['f_status'] = self.request.GET.get('f_status', '')
        return context


class CardCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, CreateView):
    model = Card
    form_class = CardForm
    template_name = 'registrations/card/form.html'
    success_url = reverse_lazy('card:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'registrations.add_card'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para cadastrar cartões.')
            return redirect(reverse_lazy('card:list'))
        return super().handle_no_permission()

class CardUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, UpdateView):
    model = Card
    context_object_name = 'card'
    form_class = CardForm
    template_name = 'registrations/card/form.html'
    success_url = reverse_lazy('card:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'registrations.change_card'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para editar um cartão.')
            return redirect(reverse_lazy('card:list'))
        return super().handle_no_permission()

class CardDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    success_url = reverse_lazy('card:list')
    login_url = reverse_lazy('login:login')
    raise_exception = False
    permission_required = 'registrations.delete_card'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para excluir um cartão')
            return redirect(reverse_lazy('card:list'))
        return super().handle_no_permission()

    def post(self, request, pk):
        card = get_object_or_404(Card, pk=pk)
        try:
            card.delete()
            messages.success(request, f"Cartão '{card}' excluído com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir cartão: {e}")
        return redirect(self.success_url)
