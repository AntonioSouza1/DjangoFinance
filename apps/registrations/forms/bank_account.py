from django import forms

from apps.registrations.models.bank_account import *

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = '__all__'