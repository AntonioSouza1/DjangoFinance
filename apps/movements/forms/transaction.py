from logging import disable

from django import forms
from apps.movements.models.transaction import Transaction

DATE_INPUT_FORMATS = ['%Y-%m-%d']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"

    description = forms.CharField(
        min_length=3,
        error_messages={
            'required': 'Campo de descrição é obrigatório.',
            'min_length': 'Certifique-se de que o campo descrição tenha no mínimo 3 caracteres.'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Descrição',
            })
    )

    add = forms.CharField(
        required=True,
        error_messages={
            'required': 'Campo acrescimos é obrigatório'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'R$ 100,00'}
        ),
        localize=True,
    )

    discount = forms.CharField(
        required=True,
        error_messages={
            'required': 'Campo de desconto é obrigatório'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'R$ 100,00'}
        ),
        localize=True,
    )

    base_value = forms.CharField(
        required=True,
        error_messages={
            'required': 'Campo valor é obrigatório'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'R$ 100,00'}
        ),
        localize=True,
    )

    amount_paid = forms.CharField(
        required=True,
        error_messages={
            'required': 'Campo valor é obrigatório'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'R$ 100,00',}
        ),
        localize=True,
    )

    def clean_value(self):
        value = self.cleaned_data["value"]
        if isinstance(value, str):
            value = value.replace(".", "").replace(",", ".")
        return value

    due_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,  # Adicionado para garantir que o Django aceite a entrada neste formato
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            },
            format='%Y-%m-%d'  # <-- ESSENCIAL: Diz ao widget como formatar o valor inicial
        )
    )

    payment_date = forms.DateField(
        required=False,
        input_formats=DATE_INPUT_FORMATS,  # Adicionado para garantir que o Django aceite a entrada neste formato
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            },
            format='%Y-%m-%d'  # <-- ESSENCIAL: Diz ao widget como formatar o valor inicial
        )
    )

