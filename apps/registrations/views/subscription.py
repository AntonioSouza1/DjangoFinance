from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from apps.registrations.forms.subscription import SubscriptionForm, CategoryForm
from apps.registrations.models.subscription import Subscription, Category, SubscriptionLog
from apps.registrations.models.supplier import Supplier
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from apps.utils.mixins import *
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.views.generic.base import ContextMixin


#Lista de Categorias
class CategoryList(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, ListView):
    model = Category
    template_name = 'registrations/subscription/category/list.html'
    paginate_by = 10
    context_object_name = 'categories'
    login_url = reverse_lazy('login:login')
    permission_required = 'subscription.view_category'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para acessar a lista de categorias.")
                return redirect(reverse_lazy('subscriptions:list'))
            return super().handle_no_permission()

    def get_queryset(self):
        f_id = self.request.GET.get('f_id')
        f_category = self.request.GET.get('f_category')

        filters = {}

        if f_id:
            filters['id'] = f_id
        if f_category:
            filters['category__icontains'] = f_category

        categories = Category.objects.filter(**filters)

        return categories

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context["f_id"] = self.request.GET.get('f_id', '')
        context["f_category"] = self.request.GET.get('f_category', '')

        return context

#Excluir categoria
class CategoryDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("subscription:category_list")
    login_url = reverse_lazy('login:login')
    permission_required = 'subscription.delete_category'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para excluir uma categoria.")
                return redirect(reverse_lazy('subscription:category_list'))
            return super().handle_no_permission()

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
class CategoryCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'registrations/subscription/category/form.html'
    success_url = reverse_lazy("subscription:category_list")
    login_url = reverse_lazy('login:login')
    permission_required = 'subscription.add_category'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para criar uma categoria.")
                return redirect(reverse_lazy('subscription:category_list'))
            return super().handle_no_permission()

#Editar categoria
class CategoryUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'registrations/subscription/category/form.html'
    success_url = reverse_lazy('subscription:category_list')
    context_object_name = 'category'
    login_url = reverse_lazy('login:login')
    permission_required = 'subscription.change_subscription'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para editar uma categoria.")
                return redirect(reverse_lazy('subscription:category_list'))
            return super().handle_no_permission()

class SubscriptionMixin(ContextMixin):

    def get_queryset(self):
        # 1. Pegue os filtros do GET
        f_id = self.request.GET.get('f_id', '')
        f_service = self.request.GET.get('f_service', '')  # <-- Bug da vírgula corrigido
        f_status = self.request.GET.get('f_status', '')
        f_category = self.request.GET.get('f_category', '')

        filters = {}

        if f_id:
            filters['id'] = f_id  # <-- Use a variável, não chame o GET de novo
        if f_service:
            filters['service__icontains'] = f_service
        if f_status:
            filters['status'] = f_status
        if f_category:
            filters['category__id'] = f_category

        # 2. Pegue a queryset base da View (importante!)
        #    Isso permite que o Mixin funcione em qualquer ListView
        if hasattr(self, 'model'):
            base_queryset = self.model._default_manager.all()
        else:
            base_queryset = Subscription.objects.all()  # Fallback

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
        context["categories"] = Category.objects.all()

        return context

#Lista de Assinaturas
class SubscriptionsList(LoginRequiredMixin, PermissionRequiredMixin, SubscriptionMixin, SuccessErrorMessageMixin, ListView):
    model = Subscription
    template_name = 'registrations/subscription/list.html'
    context_object_name = 'subscriptions'
    login_url = reverse_lazy('login:login')
    permission_required = 'registrations.view_subscription'
    raise_exception = False
    paginate_by = 10

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para acessar a lista de assinaturas.")
                return redirect(reverse_lazy('dashboard:home'))
            return super().handle_no_permission()

#Cria assinatura
class SubscriptionCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'registrations/subscription/form.html'
    success_url = reverse_lazy('subscription:list')
    login_url = reverse_lazy('login:login')
    permission_required = 'subscription.add_subscription'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para criar uma assintatura.")
                return redirect(reverse_lazy('subscriptions_list'))
            return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if not Category.objects.exists():
            messages.error(request, 'Não existem categorias cadastradas.')
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

#editar assinatura
class SubscriptionUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, UpdateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'registrations/subscription/form.html'
    success_url = reverse_lazy('subscription:list')
    login_url = reverse_lazy('login:login')
    permission_required = 'subscription.change_subscription'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para editar uma assinatura.")
                return redirect(reverse_lazy('subscriptions_list'))
            return super().handle_no_permission()

#excluir assinatura
class SubscriptionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    success_url = reverse_lazy('subscription:list')
    login_url = reverse_lazy('login:login')
    permission_required = 'subscription.delete_subscription'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para excluir uma assinatura.")
                return redirect(reverse_lazy('subscription:list'))
            return super().handle_no_permission()

    def post(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)
        try:
            subscription.delete()
            messages.success(request, f"Assinatura '{subscription}' excluída com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir assinatura: {e}")
        return redirect(self.success_url)

class SubscriptionReport(LoginRequiredMixin, PermissionRequiredMixin, SubscriptionMixin, ListView):
    model = Subscription
    template_name = 'registrations/subscription/report.html'
    context_object_name = 'subscriptions'
    login_url = reverse_lazy('login:login')
    permission_required = 'registrations.view_subscription'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para criar uma assintatura.")
                return redirect(reverse_lazy('subscriptions_list'))
            return super().handle_no_permission()


class SubscriptionHistory(LoginRequiredMixin, PermissionRequiredMixin, SuccessErrorMessageMixin, ListView):
    model = SubscriptionLog
    template_name = 'registrations/subscription/history.html'
    context_object_name = 'subscription_logs'
    login_url = reverse_lazy('login:login')
    permission_required = 'subscriptionlog.view_subscriptionlog'
    raise_exception = False

    def handle_no_permission(self):
            if self.request.user.is_authenticated:
                messages.error(self.request, "Você não tem permissão para acessar o histórico de uma assinatura.")
                return redirect(reverse_lazy('subscriptions:list'))
            return super().handle_no_permission()

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return SubscriptionLog.objects.filter(subscription=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['subscription'] = Subscription.objects.get(pk=pk)
        return context