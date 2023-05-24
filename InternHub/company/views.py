from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import CompanyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Company, CompanyRequest
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
# Create your views here.


class CreateCompanyRequestView(LoginRequiredMixin, FormView):
    template_name = 'company/create-company-request.html'
    form_class = CompanyForm
    success_url = reverse_lazy('company:companies')

    def form_valid(self, form):
        company = form.save(commit=False)
        company.status = 'PENDING'
        company.save()

        company_request = CompanyRequest.objects.create(
            company=company,
            user=self.request.user
        )
        return super().form_valid(form)


class CompaniesView(LoginRequiredMixin, ListView):
    template_name = 'company/companies.html'
    model = Company
    context_object_name = 'companies'

    def get_queryset(self):
        return self.model.objects.filter(status='APPROVED')


class ListCompanyRequestsView(ListView):
    template_name = 'company/company-requests.html'
    model = CompanyRequest
    context_object_name = 'requests'
    ordering = 'id'


class CompanyRequestDetailView(DetailView):
    model = CompanyRequest
    template_name = 'company/request-detail.html'
    context_object_name = 'request'

    def post(self, request, *args, **kwargs):
        company_request = self.get_object()
        action = request.POST.get('action')

        if action == 'approve':
            company_request.company.status = 'APPROVED'
            company_request.company.save()
            company_request.delete()
        elif action == 'reject':
            company_request.company.delete()
            company_request.delete()
            

        return redirect('company:company-requests')
