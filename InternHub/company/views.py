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
from users.models import Student, User, DepartmentSecretary
from django.core.exceptions import ValidationError
from users.views import RoleRequiredMixin
from announcements.models import Notification
# Create your views here.


class CreateCompanyRequestView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'company/create-company-request.html'
    form_class = CompanyForm
    success_url = reverse_lazy('company:companies')
    allowed_roles = ['STUDENT']

    def form_valid(self, form):
        company = form.save(commit=False)
        company.status = 'PENDING'
        company.save()

        form.save_m2m()

        student = Student.objects.get(user_id=self.request.user.user_id)

        company_request = CompanyRequest.objects.create(
            company=company,
            student=student,
        )

        department_secretary = User.objects.get(department=student.department, role='DEPARTMENT_SECRETARY')
        Notification.create_notification(
            title="New Company Request",
            content=f"Student {str(self.request.user)} has submitted a new company request for {company.name}.",
            receiver=department_secretary
        )
        Notification.create_notification(
            title="Company Request Sent",
            content=f"Has been submitted a new company request for {company.name}.",
            receiver=student
        )
        return super().form_valid(form)


class CompaniesView(LoginRequiredMixin, ListView):
    template_name = 'company/companies.html'
    model = Company
    context_object_name = 'companies'

    def get_queryset(self):
        return self.model.objects.filter(status='APPROVED')


class ListCompanyRequestsView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'company/company-requests.html'
    model = CompanyRequest
    context_object_name = 'requests'
    ordering = 'id'
    allowed_roles = ['SUPERUSER', 'DEPARTMENT_SECRETARY']

class CompanyRequestDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = CompanyRequest
    template_name = 'company/request-detail.html'
    context_object_name = 'request'
    allowed_roles = ['SUPERUSER', 'DEPARTMENT_SECRETARY']

    def post(self, request, *args, **kwargs):
        company_request = self.get_object()
        student = company_request.student
        action = request.POST.get('action')

        if action == 'approve':
            company_request.company.status = 'APPROVED'
            company_request.company.save()
            company_request.delete()

            Notification.create_notification(
                title="Company Request Approved",
                content="Your company request has been approved.",
                receiver=student
            )
            
        elif action == 'reject':
            company_request.company.delete()
            company_request.delete()

            Notification.create_notification(
                title="Company Request Rejected",
                content="Your company request has been rejected.",
                receiver=student
            )

        return redirect('company:company-requests')


class CreateCAVAView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'company/create-cava-request.html'
    form_class = CAVAForm
    success_url = reverse_lazy('main:home')
    allowed_roles = ['STUDENT']

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

        department_secretary = User.objects.get(department=student.department, role='DEPARTMENT_SECRETARY')
        Notification.create_notification(
            title="CAVA Request Submitted",
            content=f'Student { student.first_name } { student.last_name } has submitted a CAVA request.'
              'Please review the details in your dashboard. Thank you.',
            receiver=department_secretary
        )

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


class ListCAVASView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'company/cava-requests.html'
    model = CompanyApprovalValidationApplication
    context_object_name = 'requests'
    ordering = 'id'
    allowed_roles = ['SUPERUSER', 'DEPARTMENT_SECRETARY']

    def get_queryset(self):
        return CompanyApprovalValidationApplication.objects.filter(status='PENDING')


class CAVADetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    template_name = 'company/cava-request-detail.html'
    model = CompanyApprovalValidationApplication
    context_object_name = 'request'
    allowed_roles = ['SUPERUSER', 'DEPARTMENT_SECRETARY']

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
            Notification.create_notification(
                title="Company Approval Validation Approved",
                content="Your company approval validation has been approved.",
                receiver=student
            )

        elif action == 'reject':
            Notification.create_notification(
                title="Company Approval Validation Rejected",
                content="Your company approval validation has been rejected.",
                receiver=student
            )
            cava_request.delete()

        return redirect('company:cava-requests')

##ToDo Add Roles
class CompanyEvaluationView(LoginRequiredMixin, FormView):
    template_name = 'company/evaluate-company.html'
    form_class = CompanyEvaluationForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form, *args, **kwargs):
        internship = Internship.objects.get(id=self.kwargs['pk'])
        internship.company_evaluation = form.save()
        internship.save()
        return super().form_valid(form)

##ToDo Add Roles
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
