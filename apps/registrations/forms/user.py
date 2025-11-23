from django import forms
from django.contrib.auth.models import Permission, User

class UserPermissionsForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissões"
    )

    class Meta:
        model = User
        fields = ['permissions']
