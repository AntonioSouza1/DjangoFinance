from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from apps.registrations.forms.subscription import SubscriptionForm, CategoryForm
from apps.registrations.models.subscription import Subscription, Category
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from apps.utils.mixins import *
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.views.generic.base import ContextMixin


#Lista de Categorias
class CategoryListView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, ListView):
    model = Category
    template_name = 'registrations/subscription/category/list.html'
    paginate_by = 10
    context_object_name = 'categories'
    login_url = reverse_lazy('login:login')

    def get_queryset(self):
        f_id = self.request.GET.get('f_id')
        f_category = self.request.GET.get('f_category')

        filters = {}

        if f_id:
            filters['id'] = f_id
        if f_category:
            filters['category__icontains'] = f_category

        categories = Category.objects.filter(user=self.request.user, **filters)

        return categories

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["f_id"] = self.request.GET.get('f_id', '')
        context["f_category"] = self.request.GET.get('f_category', '')

        return context

#Excluir categoria
class CategoryDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("subscription:category_list")
    login_url = reverse_lazy('login:login')

    def post(self, request, pk):
        print(pk)
        category = get_object_or_404(Category, pk=pk)
        try:
            category.delete()
            messages.success(request, f"Categoria '{category}' excluída com sucesso.")
        except ProtectedError:
            messages.error(request, "Não foi possível excluir a categoria. Ela está vinculada a outros cadastros.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir categoria: {e}")
        return redirect(self.success_url)

#adicionar categoria
class CategoryCreateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'registrations/subscription/category/form.html'
    success_url = reverse_lazy("subscription:category_list")
    login_url = reverse_lazy('login:login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#Editar categoria
class CategoryUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'registrations/subscription/category/form.html'
    success_url = reverse_lazy('subscription:category_list')
    context_object_name = 'category'
    login_url = reverse_lazy('login:login')


class SubscriptionMixin(ContextMixin):

    def get_queryset(self):
        # 1. Pegue os filtros do GET
        f_id = self.request.GET.get('f_id', '')
        f_description = self.request.GET.get('f_description', '')  # <-- Bug da vírgula corrigido
        f_status = self.request.GET.get('f_status', '')
        f_category = self.request.GET.get('f_category', '')

        filters = {}

        if f_id:
            filters['id'] = f_id  # <-- Use a variável, não chame o GET de novo
        if f_description:
            filters['description__icontains'] = f_description
        if f_status:
            filters['status'] = f_status
        if f_category:
            filters['category__id'] = f_category

        # 2. Pegue a queryset base da View (importante!)
        #    Isso permite que o Mixin funcione em qualquer ListView
        if hasattr(self, 'model'):
            base_queryset = self.model._default_manager.filter(user=self.request.user)
        else:
            base_queryset = Subscription.objects.filter(user=self.request.user)  # Fallback

        return base_queryset.filter(**filters)

    def get_context_data(self, **kwargs):
        # 1. Bug do super() corrigido
        context = super().get_context_data(**kwargs)

        # 2. Passe os filtros para o template (para preencher o form)
        context["f_id"] = self.request.GET.get('f_id', '')
        context["f_service"] = self.request.GET.get('f_service', '')
        context["f_status"] = self.request.GET.get('f_status', '')
        context["f_category"] = self.request.GET.get('f_category', '')

        # 3. Passe os dados necessários para os <select>
        context["categories"] = Category.objects.filter(user=self.request.user)

        return context

#Lista de Assinaturas
class SubscriptionsListView(LoginRequiredMixin, UserIsOwnerMixin, SubscriptionMixin, SuccessErrorMessageMixin, ListView):
    model = Subscription
    template_name = 'registrations/subscription/list.html'
    context_object_name = 'subscriptions'
    login_url = reverse_lazy('login:login')

#Cria assinatura
class SubscriptionCreateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'registrations/subscription/form.html'
    success_url = reverse_lazy('subscription:list')
    login_url = reverse_lazy('login:login')

    def dispatch(self, request, *args, **kwargs):
        if not Category.objects.filter(user=self.request.user).exists():
            messages.error(request, 'Não existem categorias cadastradas.')
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Injeta o user nos argumentos do formulário
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_invalid(form)

#editar assinatura
class SubscriptionUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, UpdateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'registrations/subscription/form.html'
    success_url = reverse_lazy('subscription:list')
    login_url = reverse_lazy('login:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Injeta o user nos argumentos do formulário
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = self.object.transaction.filter(user=self.request.user).order_by('-updated_at')
        print(context['transactions'])

        return context

#excluir assinatura
class SubscriptionDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, DeleteView):
    success_url = reverse_lazy('subscription:list')
    login_url = reverse_lazy('login:login')

    def post(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)
        try:
            subscription.delete()
            messages.success(request, f"Assinatura '{subscription}' excluída com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir assinatura: {e}")
        return redirect(self.success_url)

class SubscriptionReportView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, SubscriptionMixin, ListView):
    model = Subscription
    template_name = 'registrations/subscription/report.html'
    context_object_name = 'subscriptions'
    login_url = reverse_lazy('login:login')
