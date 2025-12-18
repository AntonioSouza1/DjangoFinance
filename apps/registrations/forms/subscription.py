from django import forms
from apps.registrations.models.subscription import Subscription, Category

class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = '__all__'
        exclude = ('user',)

    def __init__(self, user, *args, **kwargs):
        # Recebemos o 'user' como argumento extra antes de iniciar o form
        super(SubscriptionForm, self).__init__(*args, **kwargs)

        # AQUI É O FILTRO:
        # Estamos dizendo: "Neste campo 'category', carregue apenas
        # as categorias onde o campo 'user' for igual ao usuário logado"
        self.fields['category'].queryset = Category.objects.filter(user=user)

    description = forms.CharField(
        min_length=3,
        error_messages={
            'required': 'Campo descrição é obrigatório.',
            'min_length': 'Certifique-se de que o campo descrição tenha no mínimo 3 caracteres.'
        },
        widget=forms.TextInput(
        attrs={
            'placeholder': 'Descrição',

        })
    )

    supplier = forms.CharField(
        min_length=3,
        required=False,
        error_messages={
            'min_length': 'Certifique-se de que o campo descrição tenha no mínimo 3 caracteres.'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Fornecedor',

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

    renewal_day = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=31,
        error_messages={
            'required': 'Campo dia de renovação é obrigatório',
            'min_value': 'Dia de renovação não pode ser menor que 1',
            'max_value': 'Dia de renovação não pode ser maior que 31.',
        },
        widget=forms.NumberInput(
            attrs={
                'placeholder': '1 á 31',
            }
        )
    )

    observation = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder':'Descrição',
                    'rows': 4,
                    'cols': 40,}
        )
    )

    canceled_at = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type':'date',
            }
        )
    )

    def clean_status(self):
        status = self.cleaned_data.get('status')
        canceled_at = self.cleaned_data.get('canceled_at')
        if canceled_at:
            status = 'C'
        if not status:
            status = 'A'
        return status

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ('user',)

    category = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':'Categoria'}
        )
    )

    def clean_category(self):
        category = self.cleaned_data['category']
        if len(category) < 3:
            self.add_error('category','A categoria precisa ser maior que 3 caracteres')
        return category