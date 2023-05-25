from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from reports.forms import ConfidentialCompanyForm
from reports.forms import SummerTrainingGradingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Internship,Feedback
from .forms import WorkAndReportEvaluationForm, ExtensionForm
from .forms import StudentReportForm
from .forms import FeedbackForm
from users.models import Student
from .models import StudentReport, WorkAndReportEvaluation,Submission, InstructorFeedback
from django.views.generic import ListView
from django.views.generic import UpdateView, CreateView, View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from users.decorators import allowed_users
from django.utils import timezone
from users.views import RoleRequiredMixin
from reports.models import Status
from django.urls import reverse_lazy
from reports.models import SubmissionStatus
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

class CreateSubmitReport(LoginRequiredMixin, RoleRequiredMixin, FormView):
    form_class = StudentReportForm
    template_name = 'reports/submit_report.html'
    success_url = reverse_lazy('reports:view_internships')
    allowed_roles = ['STUDENT']
    
    def form_valid(self, form, *args, **kwargs):
        submitted_report = form.save(commit=False)
        submitted_report.creation_date = timezone.now()

        #DUE DATE MUST BE CHANGED
        submitted_report.due_date = timezone.now() + timezone.timedelta(days=7)

        internship_pk = self.kwargs.get('pk')
        submitted_report.internship = get_object_or_404(Internship, pk=internship_pk)
            
        submitted_report.status = Status.PENDING
        submitted_report.save()

        return super().form_valid(form)

class ReportsView(ListView):
    model = StudentReport
    template_name = 'reports/view_reports.html'
    context_object_name = 'reports'

class MainView(LoginRequiredMixin,FormView):
    template_name = 'reports/main.html'

    def get(self, request):
        return render(request, 'reports/main.html')

class WorkAndReportEvaluationFormCreation(CreateView):
    model = WorkAndReportEvaluation
    form_class = WorkAndReportEvaluationForm
    template_name = 'reports/create_work_and_report_ev_form.html'

    def get_success_url(self):
        return reverse('reports:edit_wre', kwargs={'pk' : self.kwargs['pk'] })

class WorkAndReportEvaluationFormUpdate(UpdateView):
    model = WorkAndReportEvaluation
    form_class = WorkAndReportEvaluationForm
    template_name = 'reports/create_work_and_report_ev_form.html'

    def get_success_url(self):
        return reverse('reports:edit_wre', kwargs={'pk' : self.kwargs['pk'] })

class EditWorkAndReportEvaluation(View):
    def get(self, request, **kwargs):
        try:
            if WorkAndReportEvaluation.objects.filter(pk=self.kwargs['pk']).exists():
                #print(self.kwargs['pk'])
                # Redirect to update view
                return redirect('reports:update_wre', pk=self.kwargs['pk'])
            else:
                return redirect('reports:create_wre', pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            # Redirect to create view
            return redirect('reports:create_wre', pk=self.kwargs['pk'])

class CreateFeedback(LoginRequiredMixin, FormView):
    template_name = 'reports/submit_feedback.html'
    form_class = FeedbackForm
    success_url = '/reports/view-internships/'

    def form_valid(self, form):
        feedback = InstructorFeedback(feedback=form.FILES['instructor_feedback'])
        feedback.save()
        return super().form_valid(form)
    

    
class ListInternshipsView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'reports/view_internships.html'
    model = Internship
    context_object_name = 'internships'
    ordering = 'id'
    allowed_roles = ['INSTRUCTOR', 'STUDENT', 'DEPARTMENT_SECRETARY']

    def get_queryset(self):
        if self.request.user.role == 'STUDENT':
            return Internship.objects.filter(student__user_id=self.request.user.user_id)
        elif self.request.user.role == 'INSTRUCTOR':
            return Internship.objects.filter(instructor__user_id=self.request.user.user_id)
        else:
            return Internship.objects.filter(student__department=self.request.user.department)
        
    def get_context_data(self):
        context = super().get_context_data()
        context['form'] = ExtensionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ExtensionForm(request.POST)
        if form.is_valid():
            due_date = form.cleaned_data['due_date']
            internships = self.get_queryset()
            for internship in internships:
                if internship.student_report is not None:
                    internship.student_report.due_date = due_date
                    internship.student_report.save()
                else:
                    internship.student_report = Submission()
                    internship.student_report.due_date = due_date
                    internship.student_report.save()
                    internship.save()
            return redirect('reports:view_internships')  # Redirect to the same page to display updated due dates

        # Re-render the page with the same context if form is not valid
        return self.get(request, *args, **kwargs)
    


class InternshipDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    template_name = 'reports/internship_detail.html'
    model = Internship
    context_object_name = 'internship'
    allowed_roles = ['INSTRUCTOR', 'DEPARTMENT_SECRETARY']
    

    def post(self, request, *args, **kwargs):
        internship = self.get_object()
        action = request.POST.get('action')
        report = internship.student_report

        # Todo Send notification
        if action == 'approve':
            report.status = SubmissionStatus.SATISFACTORY
            

        elif action == 'reject':
            report.status = SubmissionStatus.REVISION_REQUIRED
            ##ToDo: Create Feedback and set due date for new  save 
        
        elif action == 'extend':
            form = ExtensionForm(request.POST)
            if form.is_valid():
                due_date = form.cleaned_data['due_date']
                if report.student_report is not None:
                    report.student_report.due_date = due_date
                    report.student_report.save()
                else:
                    report.student_report = Submission()
                    report.student_report.due_date = due_date
                    report.student_report.save()
                    report.save()

        return redirect('reports:view_internships')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExtensionForm()
        return context
