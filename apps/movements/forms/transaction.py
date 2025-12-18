from logging import disable

from django import forms
from apps.movements.models.transaction import Transaction, TransactionGroup, TransactionPaymentMethod, TransactionCategory


DATE_INPUT_FORMATS = ['%Y-%m-%d']


#Formularios de Transações

#Categorias de Transações
class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = '__all__'
        exclude = ('user',)

        #customizações dos input
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome'}),
        }

# Grupos de Transações
class TransactionGroupForm(forms.ModelForm):
    class Meta:
        model = TransactionGroup
        fields = '__all__'
        exclude = ('user',)

        # customizações dos input
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome'}),
        }

# Formas de pagamentos das Transações
class TransactionPaymentMethodForm(forms.ModelForm):
    class Meta:
        model = TransactionPaymentMethod
        fields = '__all__'
        exclude = ('user',)

        # customizações dos input
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome'}),
        }

#Transações
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ('user',)

    widgets = {
        'category': forms.Select(attrs={
            # Aqui você injeta a classe CSS
            'class': 'select-limitado',

            # E define o atributo 'size' para forçar a barra de rolagem
            'size': '8'  # Isso fará com que 8 opções sejam visíveis
        }),

        'group': forms.Select(attrs={
            # Aqui você injeta a classe CSS
            'class': 'select-limitado',

            # E define o atributo 'size' para forçar a barra de rolagem
            'size': '8'  # Isso fará com que 8 opções sejam visíveis
        }),

        'payment_method': forms.Select(attrs={
            # Aqui você injeta a classe CSS
            'class': 'select-limitado',

            # E define o atributo 'size' para forçar a barra de rolagem
            'size': '8'  # Isso fará com que 8 opções sejam visíveis
        }),
    }

    def __init__(self, *args, user=None, **kwargs):
        # 1. Chama o construtor original do ModelForm
        super().__init__(*args, **kwargs)

        # 2. Guarda o usuário (opcional, mas bom para validações futuras)
        self.user = user

        self.fields['category'].queryset = TransactionCategory.objects.filter(user=user)
        self.fields['group'].queryset = TransactionGroup.objects.filter(user=user)
        self.fields['payment_method'].queryset = TransactionPaymentMethod.objects.filter(user=user)

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

    def clean_base_value(self):
        base_value = self.cleaned_data["base_value"]
        if isinstance(base_value, str):
            if base_value:
                base_value = base_value.replace(".", "").replace(",", ".")
            else:
                base_value = 0
        return base_value

    add = forms.CharField(
        required=False,
        error_messages={
            'required': 'Campo acrescimos é obrigatório'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'R$ 100,00'}
        ),
        localize=True,
    )

    def clean_add(self):
        add = self.cleaned_data["add"]
        if isinstance(add, str):
            if add:
                add = add.replace(".", "").replace(",", ".")
            else:
                add = 0
        return add

    discount = forms.CharField(
        required=False,
        error_messages={
            'required': 'Campo de desconto é obrigatório'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'R$ 100,00'}
        ),
        localize=True,
    )

    def clean_discount(self):
        discount = self.cleaned_data["discount"]
        if isinstance(discount, str):
            if discount:
                discount = discount.replace(".", "").replace(",", ".")
            else:
                discount = 0
        return discount

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

    def clean_amount_paid(self):
        amount_paid = self.cleaned_data["amount_paid"]
        if isinstance(amount_paid, str):
            if amount_paid:
                amount_paid = amount_paid.replace(".", "").replace(",", ".")
            else:
                amount_paid = 0
        return amount_paid

    due_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,  # Adicionado para garantir que o Django aceite a entrada neste formato
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            },
            format='%Y-%m-%d'  # <-- ESSENCIAL: Diz ao widget como formatar o valor inicial
        )
    )

    issue_date = forms.DateField(
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
