from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from reports.forms import ConfidentialCompanyForm
from reports.forms import SummerTrainingGradingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Internship
from .forms import WorkAndReportEvaluationForm
from .forms import StudentReportForm
from users.models import Student
from django.http import HttpResponseRedirect
from .models import StudentReport
# Create your views here.


class CreateConfidentialForm(LoginRequiredMixin, FormView):
    form_class = ConfidentialCompanyForm
    template_name = 'reports/create_confidential_form.html'
    success_url = '/company/companies/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        internship_id = self.kwargs["internship_id"]
        if Internship.objects.filter(id = internship_id).exists():
            internship = Internship.objects.get(id = internship_id)
            if not internship.student.DoesNotExist:
                context['student_name'] = internship.student.first_name
                context['student_surname'] = internship.student.last_name
                context['department'] = internship.student.department.name
            else:
                context['student_name'] = "Does not exist"
                context['student_surname'] = "Does not exist"
                context['department'] = "Does not exist"
            if not internship.instructor is None:
                context['instructor_name'] = internship.instructor.first_name
                context['instructor_surname'] = internship.instructor.last_name
            else:
                context['instructor_name'] = "Does not exist"
                context['instructor_surname'] = "Does not exist"
            if not internship.course is None:
                context['course'] = internship.course
            else:
                context['course'] = "Does not exist"
        else:
            context['student_name'] = "Not reachable"
            context['student_surname'] = "Not reachable"
            context['instructor_name'] = "Not reachable"
            context['department'] = "Not reachable"
            context['instructor_surname'] = "Not reachable"
            context['course'] = "Not reachable"
        return context

    """
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
    """

#not completed
class CreateSummerTrainingGradingForm(LoginRequiredMixin, FormView):
    form_class = SummerTrainingGradingForm
    template_name = 'reports/create_summer_training_form.html'
    success_url = '/student/students/' # not good name

    def form_valid(self, form):
        # Checking if the report is satisfactory.

        if form.cleaned_data['sum_score_evaluation_except_one'] < 7:
            status = 'REJECTED'
        elif form.cleaned_data['sum_score_evaluation_except_one'] < 30:
            status = 'REJECTED'
        elif not form.cleaned_data['score_evaluation_report']:
            status = 'REJECTED'
        else:
            status = 'ACCEPTED'

        # Getting the user_id from the form.
        user_id = form.cleaned_data['student_id']
    
        # If the form is not valid, return the form with the errors.
        if form.errors != {}:
            return super().form_invalid(form)

        # If there are no errors, save the form.
        form.save()
        return super().form_valid(form)

class CreateWorkAndReportEvaluationForm(LoginRequiredMixin, FormView):
    form_class = WorkAndReportEvaluationForm
    template_name = 'reports/create_work_and_report_ev_form.html'
    success_url = '/reports/create-work-and-report-ev-form/1'

    #def get_context_data(self, **kwargs):
    #    super().get_context_data()

class CreateSubmitReport(LoginRequiredMixin, FormView):
    def get(self, request):
        form = StudentReportForm()
        return render(request, 'reports/submit_report.html',{
            'form': form
        })
    def post(self, request):
        submitted_form = StudentReportForm(request.POST, request.FILES)
        if submitted_form.is_valid():
            report = StudentReport(report=request.FILES['student_report'])
            report.save()
            return HttpResponseRedirect('/reports/submit-report/')
        return render(request, 'reports/submit_report.html', {
            'form': submitted_form
        })


