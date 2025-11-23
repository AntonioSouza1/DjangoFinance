from django import forms
from apps.registrations.models.supplier import *

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

    corporate_name = forms.CharField(
        error_messages={
            'required': 'Campo Razão social / Nome Completo é obrigatório.',
            'min_length': 'Certifique-se de que o campo Razão social / Nome Completo tenha no mínimo 3 caracteres.'
        },
        widget=forms.TextInput(
            attrs={'placeholder':'Razão social / Nome Completo',}
        )
    )

    fantasy_name = forms.CharField(
        min_length=3,
        error_messages={
            'required': 'Campo Nome Fant. / Apelido é obrigatório.',
            'min_length': 'Certifique-se de que o campo Nome Fant. / Apelido tenha no mínimo 3 caracteres.'
        },
        widget=forms.TextInput(
            attrs={'placeholder': 'Nome Fant. / Apelido', }
        )
    )

    responsible = forms.CharField(
        min_length=3,
        error_messages={
            'min_length': 'Certifique-se de que o campo responsavel tenha no mínimo 3 caracteres.'
        },
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Responsável', }
        )
    )

    cpf_cnpj = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'CPF/CNPJ', }
        )
    )

    rg_ie = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'RG/IE', }
        )
    )

    # contato
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'exemplo@exemplo.com', }
        )
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': '(00) 0000-0000', }
        )
    )

    cell_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': '(00) 00000-0000', }
        )
    )

    # endereço
    cep = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': '00000-000', }
        )
    )

    logradouro = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'logradouro', }
        )
    )

    number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nº', }
        )
    )

    complement = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Complemento', }
        )
    )

    neighborhood = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Bairro', }
        ))

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Cidade', }
        )
    )


    # obs
    observation = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'Observação',
                   'rows': 6,
                   'cols': 40, }
        )
    )

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        if cpf_cnpj == '':
            return None
        return cpf_cnpj

    def clean_rg_ie(self):
        rg_ie = self.cleaned_data.get('rg_ie')
        if rg_ie == '':
            return None
        return rg_ie