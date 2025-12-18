import calendar
from django.contrib.messages.context_processors import messages
from django.db.models import Sum, DecimalField, ProtectedError
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_date
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from apps.movements.models.transaction import Transaction, TransactionCategory, TransactionGroup, TransactionPaymentMethod
from apps.movements.forms.transaction import TransactionForm, TransactionCategoryForm, TransactionGroupForm
from apps.utils.mixins import *
from django.views.generic.base import ContextMixin
from django.db.models import Sum
from django.utils import timezone

from datetime import date

#Categorias de Transações

# Lista de Categorias
class TransactionCategoryListView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, ListView):
    model = TransactionCategory
    template_name = 'movements/transaction/category/list.html'
    paginate_by = 10
    context_object_name = 'categories'
    login_url = reverse_lazy('login:login')

    #filtros passados via GET
    def get_queryset(self):
        f_name = self.request.GET.get('f_name')

        filters = {}

        if f_name:
            filters['name__icontains'] = f_name

        categories = TransactionCategory.objects.filter(user=self.request.user, **filters)

        return categories

    #Contexto enviado para o template
    def get_context_data(self, **kwargs):
        context = super(TransactionCategoryListView, self).get_context_data(**kwargs)
        context["f_name"] = self.request.GET.get('f_name', '')
        context["total"] = TransactionCategory.objects.filter(user=self.request.user).count()

        return context

# Adicionar categoria
class TransactionCategoryCreateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, CreateView):
    model = TransactionCategory
    form_class = TransactionCategoryForm
    template_name = 'movements/transaction/category/form.html'
    success_url = reverse_lazy("transaction:category_list")
    login_url = reverse_lazy('login:login')

    # Adcionar o id do usuário logado ao formulário que será salvo
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Editar categoria
class TransactionCategoryUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, UpdateView):
    model = TransactionCategory
    form_class = TransactionCategoryForm
    template_name = 'movements/transaction/category/form.html'
    success_url = reverse_lazy('transaction:category_list')
    context_object_name = 'category'
    login_url = reverse_lazy('login:login')

# Excluir categoria
class TransactionCategoryDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, DeleteView):
    model = TransactionCategory
    success_url = reverse_lazy("transaction:category_list")
    login_url = reverse_lazy('login:login')

    def post(self, request, pk):

        category = get_object_or_404(TransactionCategory, pk=pk)

        try:
            category.delete()
            messages.success(request, f"Categoria '{category}' excluída com sucesso.")
        except ProtectedError:
            messages.error(request, "Não foi possível excluir a categoria. Ela está vinculada a outros cadastros.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir categoria: {e}")
        return redirect(self.success_url)

#Grupos de Transações

# Lista de Grupos
class TransactionGroupListView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, ListView):
    model = TransactionGroup
    template_name = 'movements/transaction/group/list.html'
    paginate_by = 10
    context_object_name = 'groups'
    login_url = reverse_lazy('login:login')

    # filtros passados via GET
    def get_queryset(self):
        f_name = self.request.GET.get('f_name')

        filters = {}

        if f_name:
            filters['name__icontains'] = f_name

        groups = TransactionGroup.objects.filter(user=self.request.user, **filters)

        return groups

    # Contexto enviado para o template
    def get_context_data(self, **kwargs):
        context = super(TransactionGroupListView, self).get_context_data(**kwargs)
        context["f_name"] = self.request.GET.get('f_name', '')
        context["total"] = TransactionGroup.objects.filter(user=self.request.user).count()

        return context


# Adicionar grupo
class TransactionGroupCreateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, CreateView):
    model = TransactionGroup
    form_class = TransactionGroupForm
    template_name = 'movements/transaction/group/form.html'
    success_url = reverse_lazy("transaction:group_list")
    login_url = reverse_lazy('login:login')

    #Adcionar o id do usuário logado ao formulário que será salvo
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Editar grupo
class TransactionGroupUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, UpdateView):
    model = TransactionGroup
    form_class = TransactionGroupForm
    template_name = 'movements/transaction/group/form.html'
    success_url = reverse_lazy('transaction:group_list')
    context_object_name = 'group'
    login_url = reverse_lazy('login:login')


# Excluir grupo
class TransactionGroupDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, DeleteView):
    model = TransactionGroup
    success_url = reverse_lazy("transaction:group_list")
    login_url = reverse_lazy('login:login')

    def post(self, request, pk):

        group = get_object_or_404(TransactionGroup, pk=pk)

        try:
            group.delete()
            messages.success(request, f"Grupo '{group}' excluído com sucesso.")
        except ProtectedError:
            messages.error(request, "Não foi possível excluir o grupo. Ela está vinculada a outros cadastros.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir grupo: {e}")
        return redirect(self.success_url)

#Formas de Pagamento de Transações

# Lista de Formas de Pagamento
class TransactionPaymentMethodListView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, ListView):
    model = TransactionPaymentMethod
    template_name = 'movements/transaction/payment/list.html'
    paginate_by = 10
    context_object_name = 'payments'
    login_url = reverse_lazy('login:login')

    def dispatch(self, request, *args, **kwargs):
        # Se NÃO existirem métodos, crie e depois continue (retorne o resultado da view)
        if not TransactionPaymentMethod.objects.filter(user=self.request.user).exists():
            standard_payment_methods = ['Dinheiro', 'Boleto', 'Cartão de Crédito', 'Cartão de debito', 'Pix']

            for default_payment_method in standard_payment_methods:
                TransactionPaymentMethod.objects.get_or_create(
                    user=request.user,
                    name__iexact=default_payment_method,
                    defaults={'name': default_payment_method}
                )

            # Não precisamos de 'return' aqui, pois a linha abaixo fará o retorno final
            # Mas vamos manter o retorno para clareza e evitar confusão na lógica
            return super().dispatch(request, *args, **kwargs)

        # Se a condição 'if' não foi atendida (os métodos já existiam),
        # o fluxo simplesmente continua e retorna o resultado da view normalmente.
        return super().dispatch(request, *args, **kwargs)

    # filtros passados via GET
    def get_queryset(self):
        f_name = self.request.GET.get('f_name')

        filters = {}

        if f_name:
            filters['name__icontains'] = f_name

        payments = TransactionPaymentMethod.objects.filter(user=self.request.user, **filters)

        return payments

    # Contexto enviado para o template
    def get_context_data(self, **kwargs):
        context = super(TransactionPaymentMethodListView, self).get_context_data(**kwargs)
        context["f_name"] = self.request.GET.get('f_name', '')
        context["total"] = TransactionPaymentMethod.objects.filter(user=self.request.user).count()

        return context


# Adicionar Forma de Pagamento
class TransactionPaymentMethodCreateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, CreateView):
    model = TransactionPaymentMethod
    form_class = TransactionGroupForm
    template_name = 'movements/transaction/payment/form.html'
    success_url = reverse_lazy("transaction:payment_method_list")
    login_url = reverse_lazy('login:login')

    #Adcionar o id do usuário logado ao formulário que será salvo
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Editar Forma de Pagamento
class TransactionPaymentMethodUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, UpdateView):
    model = TransactionPaymentMethod
    form_class = TransactionGroupForm
    template_name = 'movements/transaction/payment/form.html'
    success_url = reverse_lazy('transaction:payment_method_list')
    context_object_name = 'payment_method'
    login_url = reverse_lazy('login:login')


# Excluir Forma de Pagamento
class TransactionPaymentMethodDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, DeleteView):
    model = TransactionPaymentMethod
    success_url = reverse_lazy("transaction:payment_method_list")
    login_url = reverse_lazy('login:login')

    def post(self, request, pk):

        PaymentMethod = get_object_or_404(TransactionPaymentMethod, pk=pk)

        try:
            PaymentMethod.delete()
            messages.success(request, f"Metodo de Pagamento: '{PaymentMethod}' excluído com sucesso.")
        except ProtectedError:
            messages.error(request, "Não foi possível excluir o metodo de pagamento. Ele está vinculada a outros cadastros.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir grupo: {e}")
        return redirect(self.success_url)

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
        # 3. Captura os parâmetros do GET
        f_id = self.request.GET.get('f_id', '')
        f_description = self.request.GET.get('f_description', '')
        f_due_date_of = self.request.GET.get('f_due_date_of', '')  # vencimento de
        f_due_date = self.request.GET.get('f_due_date', '')  # até
        f_type = self.request.GET.get('f_type', '')
        f_status = self.request.GET.get('f_status', 'T')
        f_category = self.request.GET.get('f_category', '')
        f_group = self.request.GET.get('f_group', '')
        f_payment = self.request.GET.get('f_payment', '')

        filters = {}

        today = date.today()

        first_day = today.replace(day=1)

        # CORREÇÃO AQUI:
        # O _ serve para ignorar o primeiro valor (dia da semana)
        # Pegamos apenas o 'last_day_number' (ex: 30, 31 ou 28)
        _, last_day_number = calendar.monthrange(today.year, today.month)

        # Agora passamos o número inteiro correto
        last_day = today.replace(day=last_day_number)

        if f_id:
            filters['id'] = f_id
        if f_description:
            filters['description__icontains'] = f_description
        if f_due_date_of:
            filters['due_date__gte'] = f_due_date_of #de
        if f_due_date:
            filters['due_date__lte'] = f_due_date #ate
        if f_status and f_status != 'T':
            filters['status'] = f_status
        if f_type:
            filters['type'] = f_type
        if f_category:
            filters['category'] = f_category
        if f_group:
            filters['group'] = f_group
        if f_payment:
            filters['payment_method'] = f_payment

        if not filters:
            filters['due_date__gte'] = first_day  # de
            filters['due_date__lte'] = last_day  # ate
            if not f_status:
                filters['status__in'] = ['P', 'V']

        if hasattr(self, 'model'):
            base_queryset = self.model._default_manager.filter(user=self.request.user)
        else:
            base_queryset = Transaction.objects.filter(user=self.request.user)
        return base_queryset.filter(**filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Reutiliza a queryset já filtrada pelo método acima
        queryset_filtrada = self.get_queryset()  # Agora é um método, usa ()

        # Agregações
        # Dica: Use (Result or 0) para evitar que retorne "None" se não houver dados
        total_output_agg = queryset_filtrada.filter(type='S').aggregate(
            total=Coalesce(
                Sum('amount_paid'),
                0,
                output_field=DecimalField()  # <--- O DJANGO PRECISA DISSO
            )
        )

        total_input_agg = queryset_filtrada.filter(type='E').aggregate(
            total=Coalesce(
                Sum('amount_paid'),
                0,
                output_field=DecimalField()  # <--- AQUI TAMBÉM
            )
        )

        context["f_id"] = self.request.GET.get('f_id', '')
        context["f_description"] = self.request.GET.get('f_description', '')
        context["f_due_date_of"] = self.request.GET.get('f_due_date_of', '')
        context["f_due_date"] = self.request.GET.get('f_due_date','')
        context["f_type"] = self.request.GET.get('f_type', '')
        context["f_status"] = self.request.GET.get('f_status', 'T')
        context["total_output"] = total_output_agg['total']
        context["total_input"] = total_input_agg['total']
        context["f_category"] = self.request.GET.get('f_category', '')
        context["f_group"] = self.request.GET.get('f_group', '')
        context["f_payment"] = self.request.GET.get('f_payment', '')
        context["payment_methods"] = TransactionPaymentMethod.objects.filter(user=self.request.user)
        context["groups"] = TransactionGroup.objects.filter(user=self.request.user)
        context["categories"] = TransactionCategory.objects.filter(user=self.request.user)

        return context

class TransactionListView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, TransactionListMixin, ListView):
    model = Transaction
    template_name = "movements/transaction/list.html"
    context_object_name = "transactions"
    login_url = reverse_lazy('login:login')
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        Transaction.objects.filter(
            user=self.request.user,
            status='P',
            due_date__lt=timezone.now().date()  # Filtra transações vencidas
        ).update(status='V')
        return super().dispatch(request, *args, **kwargs)


class TransactionCreateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "movements/transaction/form.html"
    success_url = reverse_lazy("transaction:list")
    login_url = reverse_lazy('login:login')

    def dispatch(self, request, *args, **kwargs):
        # Se NÃO existirem métodos, crie e depois continue (retorne o resultado da view)
        if not TransactionPaymentMethod.objects.filter(user=self.request.user).exists():
            standard_payment_methods = ['Dinheiro', 'Boleto', 'Cartão de Crédito', 'Cartão de debito', 'Pix']

            for default_payment_method in standard_payment_methods:
                TransactionPaymentMethod.objects.get_or_create(
                    user=request.user,
                    name__iexact=default_payment_method,
                    defaults={'name': default_payment_method}
                )

            # Não precisamos de 'return' aqui, pois a linha abaixo fará o retorno final
            # Mas vamos manter o retorno para clareza e evitar confusão na lógica
            return super().dispatch(request, *args, **kwargs)

        # Se a condição 'if' não foi atendida (os métodos já existiam),
        # o fluxo simplesmente continua e retorna o resultado da view normalmente.
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Adiciona o usuário logado aos argumentos
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "movements/transaction/form.html"
    success_url = reverse_lazy("transaction:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Adiciona o usuário logado aos argumentos
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        transaction = self.get_object()
        if transaction.status == 'Q':
            messages.error(request, 'Não e possivel editar uma transação já baixada')
            return redirect('transaction:list')
        return super().dispatch(request, *args, **kwargs)

class TransactionDetailView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, DetailView):
    model = Transaction
    form_class = TransactionForm
    template_name = "movements/transaction/detail.html"


class TransactionDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, DeleteView):
    success_url = reverse_lazy('transaction:list')
    login_url = reverse_lazy('login:login')

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

class TransactionReportView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, TransactionListMixin, ListView):
    model = Transaction
    template_name = "movements/transaction/report.html"
    context_object_name = "transactions"
    login_url = reverse_lazy('login:login')

class SettleTransactionView(LoginRequiredMixin, UserIsOwnerMixin, SuccessErrorMessageMixin, View):
    def post(self, request, pk):

        transaction = get_object_or_404(Transaction, pk=pk)

        try:
            if transaction.status == 'Q':
                messages.error(request, 'Transação já baixada')
            else:
                payment_method = self.request.POST['payment_method']
                date = parse_date(self.request.POST['date'])

                if payment_method:
                    if date:
                        if date < timezone.now().date():
                            transaction.status = 'Q'
                            transaction.payment_method = self.request.POST['payment_method']
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
                else:
                    messages.error(request, 'Não informado o metodo de pagamento')

        except Exception as e:
            messages.error(request, 'Erro ao baixar transação')

        return redirect(reverse_lazy('transaction:list'))
