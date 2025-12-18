from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.db import models
from apps.registrations.models.subscription import Subscription

'''
Obs: para trabalhar com multiplos cliente, está sendo filtrado pelo id do usuário.
Todas as tabelas por padrão tem que conter o campo user.
'''

#Tabela de Categorias
class TransactionCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "categorias"
        ordering = ['name']


    def __str__(self):
        return self.name

#tabela de Grupos
class TransactionGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Grupos"
        verbose_name_plural = "Grupos"
        ordering = ['name']

#tabela de metodos de pagamento
class TransactionPaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Metodo de pagamento"
        verbose_name_plural = "Metodos de Pagamentos"
        ordering = ['name']

class Transaction(models.Model):

    TYPES_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saida'),
    ]

    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('Q', 'Quitado'),
        ('V', 'Vencido'),
        ('C', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES_CHOICES, verbose_name="Tipo")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Desconto")
    add = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Acrescimos")
    base_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Base")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Pago")
    issue_date = models.DateField(verbose_name="Data de Emissão")
    due_date = models.DateField(verbose_name="Data de Vencimento")
    payment_date = models.DateField(verbose_name="Data de Pagamento", null=True, blank=True)

    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, verbose_name="Assinatura", limit_choices_to={'status': 'A'}, related_name='templates', null=True, blank=True)

    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, verbose_name="Categoria", blank=True, null=True)
    group = models.ForeignKey(TransactionGroup, on_delete=models.SET_NULL, verbose_name="Grupo", blank=True, null=True)
    payment_method = models.ForeignKey(TransactionPaymentMethod, on_delete=models.SET_NULL, verbose_name="Pagamento", blank=True, null=True)

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name="Status", default='P')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ('-updated_at',)

    def __str__(self):
        return self.description
