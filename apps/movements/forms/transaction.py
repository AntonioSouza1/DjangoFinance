from django import forms
from apps.movements.models.transaction import Transaction

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

    value = forms.CharField(
        required=True,
        error_messages={
            'required': 'Campo valor é obrigatório'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'R$ 100,00'}
        ),
        localize=True,
    )

    def clean_value(self):
        value = self.cleaned_data["value"]
        if isinstance(value, str):
            value = value.replace(".", "").replace(",", ".")
        return value

    due_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    payment_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

