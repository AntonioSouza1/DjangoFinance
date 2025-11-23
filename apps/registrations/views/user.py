from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.registrations.forms.user import *
from apps.utils.mixins import *

# views.py
class UserCreate(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registrations/user/form.html'
    success_url = reverse_lazy('list_user')

@login_required(login_url='login')
def create_user(request):
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('login')
    else:
        register_form = UserCreationForm
    return render(request, 'login/register.html', {"user_form": register_form})

class ListUser(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'registrations/user/list.html'
    paginate_by = 10

class UserUpdate(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'registrations/user/form.html'
    success_url = reverse_lazy('list_user')

class UserPermissionsUpdate(UpdateView):
    model = User
    form_class = UserPermissionsForm
    template_name = 'registrations/user/permissions.html'
    success_url = reverse_lazy('list_user')

class UserDelete(DeleteView):
    model = User
    context_object_name = 'user'
    template_name = 'registrations/user/confirm_delete.html'
    success_url = reverse_lazy('list_user')

    def post(self, request, pk):
        category = get_object_or_404(User, pk=pk)
        try:
            category.delete()
            messages.success(request, f"Assinatura '{category}' excluída com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir assinatura: {e}")
        return redirect(self.success_url)



