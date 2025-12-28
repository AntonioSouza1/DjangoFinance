from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "categorias"
        ordering = ['name']

    def __str__(self):
        return self.name

class Subscription(models.Model):

    SUBSCRIPTION_TYPES = [
        ('I', 'Individual'),
        ('F', 'Familiar'),
        ('E', 'Estudante')
    ]

    PAYMENT_TYPES = [
        ('CC', 'Cartão de Crédito'),
        ('CD', 'Cartão de Débito'),
        ('P', 'PIX'),
        ('B', 'Boleto'),
    ]

    PAYMENT_FREQUENCIES = [
        ('M', 'Mensal'),
        ('T', 'Trimestral'),
        ('A', 'Anual')
    ]

    STATUS = [
        ('A', 'Ativo'),
        ('C', 'Cancelado'),
    ]

    user = models.ForeignKey(User, verbose_name="Usuário", on_delete=models.CASCADE)
    description = models.CharField(max_length=100, verbose_name="Descrição")
    supplier = models.CharField(max_length=100, null=True, blank=True, verbose_name='Fornecedor')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Categoria", null=True, blank=True)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, verbose_name="Tipo de Assinatura")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_TYPES, verbose_name="Metodo de Pagamento")
    renewal_day = models.IntegerField(verbose_name="Dia de renovação")
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCIES, verbose_name="Frequencia de pagamento")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="data de criacao")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="data de atualizacao")
    canceled_at = models.DateField(null=True, blank=True, verbose_name="data de cancelamento")
    observation = models.TextField(null=True, blank=True, verbose_name='Observação')
    status = models.CharField(max_length=1, choices=STATUS, default='A')

    class Meta:
        verbose_name = "Assinatura"
        verbose_name_plural = "Assinaturas"
        ordering = ['-updated_at']

    def __str__(self):
        return self.description

#auditlog.register(Subscription)
#auditlog.register(Category)