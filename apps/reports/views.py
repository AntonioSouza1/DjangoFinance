from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import  View

# Create your views here.
class Reports(LoginRequiredMixin, View):
    login_url = reverse_lazy('login:login')
    def get(self, request, *args, **kwargs):
        return render(request, 'reports.html')