from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def login_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # com backend custom
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            login_form = AuthenticationForm(request, data=request.POST)
    else:
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        else:
            login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})


def logout_form(request):
    logout(request)
    return redirect('login:login')
