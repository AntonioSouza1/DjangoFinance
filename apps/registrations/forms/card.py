from django import forms

from apps.registrations.models.card import *

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'

    card_name = forms.CharField(
        min_length=3,
        error_messages={
            'required': 'Campo nome do cartão é obrigatório.',
            'min_length': 'Certifique-se de que o campo nome do cartão tenha no mínimo 3 caracteres.'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'Nome do Cartão'}
        )
    )

    card_number = forms.CharField(
        error_messages={
            'required': 'Campo número do cartão é obrigatório.'
        },
        widget=forms.NumberInput(
            attrs={'placeholder': 'Número do Cartão'}
        )
    )

    expiration_date = forms.DateField(
        error_messages={
            'required': 'Campo validade é obrigatório.'
        },
        widget=forms.DateInput(
            attrs={
                'type':'date',
            }
        )
    )

    billing_day = forms.IntegerField(
        min_value=1,
        max_value=31,
        error_messages={
            'required': 'Campo dia de fechamento é obrigatório',
            'min_value': 'Dia de fechamento não pode ser menor que 1',
            'max_value': 'Dia de fechamento não pode ser maior que 31.',
        },
        widget=forms.NumberInput(
            attrs={'placeholder': 'Fechamento',
                   'max-length': 31,
                    'min-length': 0,}
        )
    )

    due_day = forms.IntegerField(
        min_value=1,
        max_value=31,
        error_messages={
            'required': 'Campo dia de vencimento é obrigatório',
            'min_value': 'Dia de vencimento não pode ser menor que 1',
            'max_value': 'Dia de vencimento não pode ser maior que 31.',
        },
        widget=forms.NumberInput(
            attrs={'placeholder': 'Vencimento',
                'max-length': 31,
                'min-length': 0,}
        )
    )

    credit_limit = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={'placeholder': '1.000,00'}
        )
    )

    observation = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'Observações'}
        )
    )
