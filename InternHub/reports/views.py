from django.shortcuts import render
from django.views.generic.edit import FormView
from reports.forms import ConfidentialCompanyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Internship
from users.models import Student
# Create your views here.


class CreateConfidentialForm(LoginRequiredMixin, FormView):
    form_class = ConfidentialCompanyForm
    template_name = 'reports/create_confidential_form.html'
    success_url = '/company/companies/'

    def form_valid(self, form):
        # Checking if the report is satisfactory.

        if form.cleaned_data['grade'] < 7:
            status = 'REJECTED'
        elif not form.cleaned_data['is_work_related']:
            status = 'REJECTED'
        elif not form.cleaned_data['supervisor_background']:
            status = 'REJECTED'
        else:
            status = 'ACCEPTED'

        # Getting the user_id and course from the form.
        user_id = form.cleaned_data['student_id']
        course = form.cleaned_data['course']

        # Getting the internship object.
        internship = Internship.objects.get(
            student=Student.objects.get(user_id=user_id), course=course)

        # If the form is not valid, return the form with the errors.
        if form.errors != {}:
            return super().form_invalid(form)

        # If there are no errors, save the form and update the internship status.
        form.save()
        internship.confidential_company_form.status = status
        return super().form_valid(form)
