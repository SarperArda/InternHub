from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import CompanyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Company
# Create your views here.


class CreateCompanyView(LoginRequiredMixin, FormView):
    form_class = CompanyForm
    template_name = 'company/create_company.html'
    success_url = '/company/companies/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CompaniesView(LoginRequiredMixin, ListView):
    template_name = 'company/companies.html'
    model = Company
    context_object_name = 'companies'
