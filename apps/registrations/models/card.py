from django.db import models

class Card(models.Model):
    CARD_TYPES = [
        ('CR', 'Crédito'),
        ('DB', 'Débito'),
        ('PP', 'Pré-pago'),
    ]

    STATUS = [
        ('A', 'Ativo'),
        ('V', 'Vencido'),
        ('I', 'Inativo'),
    ]

    card_name = models.CharField(max_length=50, verbose_name="Nome do cartão")
    card_number = models.CharField(max_length=16, verbose_name='Número do cartão')
    card_type = models.CharField(max_length=2, choices=CARD_TYPES, verbose_name='Tipo de Cartão')
    expiration_date = models.DateField(verbose_name='Validade')
    billing_day = models.PositiveSmallIntegerField(verbose_name='Vencimento')
    due_day = models.PositiveSmallIntegerField(verbose_name='Renovação')
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Limite de credito")
    status = models.CharField(max_length=2, choices=STATUS, default='A', verbose_name="Status")
    observation = models.TextField(blank=True, null=True, verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cartão"
        verbose_name_plural = "Cartões"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.card_name} - ****{self.card_number[-4:]}"
