from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import CompanyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Company
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
# Create your views here.


class CreateCompanyView(LoginRequiredMixin, FormView):

    def get(self, request):
        template_name = 'company/create_company.html'
        form = CompanyForm
        return render(request, template_name,{
            'form': form
    })

    def post(self, request):  
        success_url = '/company/companies/'  
        return HttpResponseRedirect(success_url)
    
    
    '''
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    '''

class CompaniesView(LoginRequiredMixin, ListView):
    template_name = 'company/companies.html'
    model = Company
    context_object_name = 'companies'
