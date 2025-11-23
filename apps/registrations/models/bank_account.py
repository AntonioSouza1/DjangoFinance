from django.db import models
from django.contrib.auth.models import User

class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('CC', 'Conta Corrente'),
        ('CP', 'Conta Poupança'),
        ('INV', 'Investimento'),
    ]

    CURRENCIES = [
        ('BRL', 'Real Brasileiro'),
        ('USD', 'Dólar Americano'),
        # outros...
    ]

    STATUS = [
        ('A', 'Ativo'),
        ('I', 'Inativo'),
    ]

    bank_name = models.CharField(max_length=100, verbose_name='Nome do banco')
    agency_number = models.CharField(max_length=20, verbose_name='Número do agencia')
    account_number = models.CharField(max_length=30, verbose_name='Número da conta')
    account_type = models.CharField(max_length=3, choices=ACCOUNT_TYPES, verbose_name='Tipo de conta')
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='BRL', verbose_name='Moeda')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    status = models.CharField(max_length=2, choices=STATUS, verbose_name='status', default='A')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conta Bancaria"
        verbose_name_plural = "Contas Bancaria"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
