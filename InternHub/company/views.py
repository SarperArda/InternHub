from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import CompanyForm, CAVAForm, CompanyEvaluationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Company, CompanyRequest, CompanyApprovalValidationApplication
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from users.decorators import allowed_users
from django.utils import timezone
from reports.models import Internship, Status
from users.models import Student
from django.core.exceptions import ValidationError
# Create your views here.


class CreateCompanyRequestView(LoginRequiredMixin, FormView):
    template_name = 'company/create-company-request.html'
    form_class = CompanyForm
    success_url = reverse_lazy('company:companies')

    def form_valid(self, form):
        company = form.save(commit=False)
        company.status = 'PENDING'
        company.save()

        form.save_m2m()

        company_request = CompanyRequest.objects.create(
            company=company,
            user=self.request.user
        )
        return super().form_valid(form)

    @method_decorator(allowed_users(['STUDENT']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CompaniesView(LoginRequiredMixin, ListView):
    template_name = 'company/companies.html'
    model = Company
    context_object_name = 'companies'

    def get_queryset(self):
        return self.model.objects.filter(status='APPROVED')


class ListCompanyRequestsView(LoginRequiredMixin, ListView):
    template_name = 'company/company-requests.html'
    model = CompanyRequest
    context_object_name = 'requests'
    ordering = 'id'

    @method_decorator(allowed_users(['SUPERUSER', 'DEPARTMENT_SECRETARY']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CompanyRequestDetailView(LoginRequiredMixin, DetailView):
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

    @method_decorator(allowed_users(['SUPERUSER', 'DEPARTMENT_SECRETARY']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateCAVAView(LoginRequiredMixin, FormView):
    template_name = 'company/create-cava-request.html'
    form_class = CAVAForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        student = Student.objects.get(user_id=self.request.user.user_id)
        course = form.instance.course

        pending_internship = Internship.objects.filter(
            student=student,
            course=course,
            status=Status.PENDING
        ).exists()

        if pending_internship:
            # Raise a ValidationError if a pending internship exists
            raise ValidationError(
                "You have a pending internship for this course. You cannot submit another CAVA.")

        cava = form.save(commit=False)
        cava.status = 'PENDING'
        cava.student = student
        cava.demand_date = timezone.now()

        cava.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateCAVAView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    """
    @method_decorator(allowed_users(['STUDENT']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    """


class ListCAVASView(LoginRequiredMixin, ListView):
    template_name = 'company/cava-requests.html'
    model = CompanyApprovalValidationApplication
    context_object_name = 'requests'
    ordering = 'id'

    @method_decorator(allowed_users(['SUPERUSER', 'DEPARTMENT_SECRETARY']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return CompanyApprovalValidationApplication.objects.filter(status='PENDING')


class CAVADetailView(LoginRequiredMixin, DetailView):
    template_name = 'company/cava-request-detail.html'
    model = CompanyApprovalValidationApplication
    context_object_name = 'request'

    def post(self, request, *args, **kwargs):
        cava_request = self.get_object()
        action = request.POST.get('action')

        # Todo Send notification
        if action == 'approve':
            cava_request.status = 'APPROVED'
            student = cava_request.student
            company = cava_request.requested_company
            course = cava_request.course

            cava_request.course = None
            cava_request.company = None
            cava_request.student = None
            cava_request.save()

            internship = Internship.objects.create(
                student=student,
                company=company,
                course=course,
                company_approval=cava_request,
            )

        elif action == 'reject':
            cava_request.delete()

        return redirect('company:cava-requests')

    @method_decorator(allowed_users(['SUPERUSER', 'DEPARTMENT_SECRETARY']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CompanyEvaluationView(LoginRequiredMixin, FormView):
    template_name = 'company/evaluate-company.html'
    form_class = CompanyEvaluationForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form, *args, **kwargs):
        internship = Internship.objects.get(id=self.kwargs['pk'])
        internship.company_evaluation = form.save()
        internship.save()
        return super().form_valid(form)

class ListCompanyEvaluationsView(LoginRequiredMixin, ListView):
    template_name = 'company/company-evaluations.html'
    model = Internship
    context_object_name = 'internships'

    def get_queryset(self):
        student = Student.objects.get(user_id=self.request.user.user_id)
        return self.model.objects.filter(student=student)



class MainView(LoginRequiredMixin, FormView):
    template_name = 'company/main.html'

    def get(self, request):
        return render(request, 'company/main.html')
