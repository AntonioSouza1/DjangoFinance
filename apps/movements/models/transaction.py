from auditlog.registry import auditlog
from django.db import models
from apps.registrations.models.subscription import Subscription

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

    type = models.CharField(max_length=2, choices=TYPES_CHOICES, verbose_name="Tipo")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Desconto")
    add = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Acrescimos")
    base_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Base")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Pago")
    due_date = models.DateField(verbose_name="Data de Vencimento")
    payment_date = models.DateField(verbose_name="Data de Pagamento", null=True, blank=True)

    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT, verbose_name="Assinatura", limit_choices_to={'status': 'A'}, related_name='transaction', null=True, blank=True)

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name="Status", default='P')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ('-updated_at',)

    def __str__(self):
        return self.description

auditlog.register(Transaction)