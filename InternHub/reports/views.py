from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, UpdateView, CreateView, View
from django.views.generic.base import TemplateView
from reports.forms import ConfidentialCompanyForm
from reports.forms import SummerTrainingGradingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WorkAndReportEvaluationForm, InternshipAssignmentForm
from .models import Internship,Feedback, ConfidentialCompany
from .forms import WorkAndReportEvaluationForm, ExtensionForm
from .forms import StudentReportForm
from .forms import FeedbackForm
from users.models import Student
from .models import StudentReport, WorkAndReportEvaluation, Submission, InstructorFeedback
from django.views.generic import ListView
from django.views.generic import UpdateView, CreateView, View

from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import StudentReport, WorkAndReportEvaluation
from .models import InstructorFeedback
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from users.models import DepartmentSecretary, Instructor
from users.decorators import allowed_users
from main import decorators
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.utils import timezone
from users.views import RoleRequiredMixin
from reports.models import Status
from django.urls import reverse_lazy
from reports.models import SubmissionStatus
from announcements.models import Notification
from users.models import Student, User, DepartmentSecretary, Instructor
# Create your views here.


class CreateConfidentialForm(CreateView):
    form_class = ConfidentialCompanyForm
    template_name = 'reports/create_confidential_form.html'
    model = ConfidentialCompany
    success_url = reverse_lazy('reports:view_internships')
    def get_success_url(self):
        confidential = self.object
        if confidential.grade < 7 or confidential.is_work_related == 'No' or confidential.supervisor_background == 'No':
            confidential.status = 'REJECTED'
        else:
            confidential.status = 'ACCEPTED'
        internship = Internship.objects.all().filter(pk=self.kwargs.get('pk')).first()
        if internship.confidential_company_form:
            internship.confidential_company_form.delete()
        internship.confidential_company_form = confidential
        print(internship.confidential_company_form.grade)
        internship.save()
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        internship_id = self.kwargs["pk"]
        if Internship.objects.filter(id = internship_id).exists():
            internship = Internship.objects.get(id = internship_id)
            context['student_name'] = internship.student.first_name + " " + internship.student.last_name
            context['department'] = internship.student.department.name
            context['instructor_name'] = internship.instructor.first_name + " " + internship.instructor.last_name
            context['course'] = internship.student.department.code + " " + internship.course.code
        return context


#not completed
class CreateSummerTrainingGradingForm(LoginRequiredMixin, FormView):
    form_class = SummerTrainingGradingForm
    template_name = 'reports/create_summer_training_form.html'
    success_url = '/student/students/'  # not good name

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


class WorkAndReportEvaluationFormCreation(CreateView):
    model = WorkAndReportEvaluation
    form_class = WorkAndReportEvaluationForm
    template_name = 'reports/create_work_and_report_ev_form.html'

    # Create a new WorkAndReportEvaluation instance
    def get_success_url(self):
        work_and_report_evaluation = self.object
        internship = Internship.objects.all().filter(pk=self.kwargs.get('pk')).first()
        # Set the internship's work_and_report_evaluation field
        work_and_report_evaluation.calculate_total_grade()
        internship.work_and_report_evaluation_form = work_and_report_evaluation
        print(internship.work_and_report_evaluation_form.total_work_grade)
        internship.save()
        return reverse('reports:edit_wre', kwargs={'pk' : self.kwargs['pk'] })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        internship = Internship.objects.all().filter(pk=self.kwargs.get('pk')).first()
        context['student_name'] = internship.student.first_name + " " + internship.student.last_name
        context['department'] = internship.student.department.name
        context['course'] = internship.student.department.code + " " + internship.course.code
        #ontext['form'] = self.get_form()
        return context

class WorkAndReportEvaluationFormUpdate(UpdateView):
    model = WorkAndReportEvaluation
    form_class = WorkAndReportEvaluationForm
    template_name = 'reports/create_work_and_report_ev_form.html'

    def get_success_url(self):
        work_and_report_evaluation = self.object
        work_and_report_evaluation.calculate_total_grade()
        internship = Internship.objects.all().filter(pk=work_and_report_evaluation.internship.pk).first()
        print(internship.work_and_report_evaluation_form.total_work_grade)
        return reverse('reports:edit_wre', kwargs={'pk' : work_and_report_evaluation.internship.pk })

    def get_context_data(self, **kwargs):
        work_and_report_evaluation = self.object
        context = super().get_context_data(**kwargs)
        internship = Internship.objects.all().filter(pk=work_and_report_evaluation.internship.pk).first()
        context['student_name'] = internship.student.first_name + " " + internship.student.last_name
        context['department'] = internship.student.department.name
        context['course'] = internship.student.department.code + " " + internship.course.code
        #context['form'] = self.get_form()
        return context
class EditWorkAndReportEvaluation(View):
    def get(self, request, **kwargs):
        target_form = Internship.objects.filter(pk=self.kwargs['pk']).first().work_and_report_evaluation_form
        if target_form:
            real_pk = target_form.pk
            # Redirect to update view
            return redirect('reports:update_wre', pk=real_pk)
        else:
            return redirect('reports:create_wre', pk=self.kwargs['pk'])



class CreateSubmitReport(LoginRequiredMixin, FormView):
    def get(self, request):
        form = StudentReportForm()
        return render(request, 'reports/submit_report.html', {
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


class CreateSubmitReport(LoginRequiredMixin, RoleRequiredMixin, FormView):
    form_class = StudentReportForm
    template_name = 'reports/submit_report.html'
    success_url = reverse_lazy('reports:view_internships')
    allowed_roles = ['STUDENT']

    def form_valid(self, form, *args, **kwargs):
        submitted_report = form.save(commit=False)
        submitted_report.creation_date = timezone.now()

        # DUE DATE MUST BE CHANGED
        submitted_report.due_date = timezone.now() + timezone.timedelta(days=7)

        internship_pk = self.kwargs.get('pk')
        submitted_report.internship = get_object_or_404(
            Internship, pk=internship_pk)

        submitted_report.status = Status.PENDING
        submitted_report.save()

        internship = Internship.objects.get(pk=internship_pk)
        return super().form_valid(form)


class ReportsView(ListView):
    model = StudentReport
    template_name = 'reports/view_reports.html'
    context_object_name = 'reports'


class MainView(LoginRequiredMixin, FormView):
    template_name = 'reports/main.html'

    def get(self, request):
        return render(request, 'reports/main.html')


class InternshipAssignmentView(FormView, LoginRequiredMixin):
    form_class = InternshipAssignmentForm
    template_name = 'reports/internship_assignment.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['instructor'].queryset = Instructor.objects.filter(
            department=self.request.user.department)
        form.fields['internships'].queryset = Internship.objects.filter(
            student__department=self.request.user.department)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse('main:home')

    def form_valid(self, form):
        action = self.request.POST.get('action')

        if action == 'Assign':
            instructor = form.cleaned_data['instructor']
            internships = form.cleaned_data['internships']

            for internship in internships:
                internship.instructor = instructor
                internship.save()

        elif action == 'RandomlyAssign':
            instructors = Instructor.objects.filter(
                department=self.request.user.department)
            internships = Internship.objects.filter(
                student__department=self.request.user.department)
            instructor_count = instructors.count()
            internship_count = len(internships)
            internship_per_instructor = internship_count // instructor_count

            instructor_index = 0
            # Iterate over the internships and assign instructors
            for internship in internships:
                import random
                instructor = instructors[instructor_index]
                internship.instructor = instructor
                internship.save()

                # Increment instructor index and loop back if needed
                instructor_index += 1
                if instructor_index >= instructor_count:
                    instructor_index = 0

        elif action == 'Clear':
            internships = Internship.objects.filter(
                student__department=self.request.user.department)
            for internship in internships:
                internship.instructor = None
                internship.save()

        return super().form_valid(form)

    @method_decorator(allowed_users(['DEPARTMENT_SECRETARY']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class InternshipListView(ListView, LoginRequiredMixin):
    pass

class CreateFeedback(LoginRequiredMixin, FormView):
    template_name = 'reports/submit_feedback.html'
    form_class = FeedbackForm
    success_url = '/reports/view-internships/'
    allowed_roles = ['INSTRUCTOR']

    def form_valid(self, form):

        feedback = InstructorFeedback(
            feedback=form.FILES['instructor_feedback'])
        feedback.save()

        internship_pk = self.kwargs.get('pk')
        internship = Internship.objects.all().get(pk=internship_pk)
        Notification.create_notification(
            title="New Submitted Report",
            content=f"Student {str(self.request.user)} has submitted a new feedback for {internship.course}.",
            receiver= internship.student,
        )
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
        context['submission_statuses'] = {}
        context['feedback_needed'] = {}
        context['feedback_recieved'] = {}

        for internship in context['internships']:
            if internship.submissions.exists():
                last_submission = internship.submissions.all().latest('id')
                submissions = internship.submissions.all().order_by('-id')
                second_last_submission = submissions[1] if submissions.count() > 1 else None 

                if last_submission.file == "" and second_last_submission is not None:
                    context['feedback_recieved'][internship.pk] = True                
                else:
                    context['feedback_recieved'][internship.pk] = False

                context['submission_statuses'][internship.pk] = last_submission.get_status_display()
                # Check if feedback is needed for the last submission
                feedback_needed = bool(
                    last_submission.file.name) and last_submission.status == SubmissionStatus.PENDING
                context['feedback_needed'][internship.pk] = feedback_needed
            else:
                context['submission_statuses'][internship.pk] = None
                context['feedback_needed'][internship.pk] = False
                Notification.create_notification(
                        title="New Submission",
                        content=f"Instructor {str(self.request.user)} has submitted a new submission for {internship.student.department.code}{internship.course}.",
                        receiver=internship.student,
                )
        return context

    def post(self, request, *args, **kwargs):
        form = ExtensionForm(request.POST)
        if form.is_valid():
            due_date = form.cleaned_data['due_date']
            internships = self.get_queryset()
            for internship in internships:
                # Get the existing submission with status "PENDING"
                report = internship.submissions.filter(
                    status=SubmissionStatus.PENDING).first()
                # Create a new submission if it doesn't exist
                if report is None:
                    report = Submission.objects.create(
                        internship=internship, due_date=due_date)
                else:
                    report.due_date = due_date
                    report.save()
                # Add the submission to the internship if it doesn't exist
                if report.id is None:
                    internship.submissions.add(report)
                Notification.create_notification(
                        title="New Due Date",
                        content=f"Instructor {str(self.request.user)} has submitted a new due date for {internship.student.department.code}{internship.course} at {due_date}.",
                        receiver=internship.student,
                )
            # Redirect to the view page
            return redirect('reports:view_internships')

        # Re-render the page with the same context if form is not valid
        return self.get(request, *args, **kwargs)


class InternshipDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    template_name = 'reports/internship_detail.html'
    model = Internship
    context_object_name = 'internship'
    allowed_roles = ['INSTRUCTOR', 'DEPARTMENT_SECRETARY', 'STUDENT']

    def post(self, request, *args, **kwargs):
        internship = self.get_object()
        action = request.POST.get('action')
        report_form = StudentReportForm(request.POST, request.FILES)
        # Form for the due date and feedback
        form = ExtensionForm(request.POST)

        if action == 'satisfactory':
            # handle the satisfactory action here
            last_submission = internship.submissions.latest('creation_date')
            last_submission.status = SubmissionStatus.SATISFACTORY
            last_submission.internship.status = SubmissionStatus.SATISFACTORY
            last_submission.internship.save()
            last_submission.save()
            # Set internship status as Satisfactory too if needed
            Notification.create_notification(
                title="Report is Satisfactory",
                content=f"{internship.student.department.code} {internship.course}'s report is marked as satisfactory by {self.request.user}.",
                receiver=internship.student,
            )

        elif action == 'revision_required':
            # handle the revision_required action here
            if form.is_valid():
                feedback_description = form.cleaned_data['feedback_description']
                last_submission = internship.submissions.latest(
                    'creation_date')
                last_submission.status = SubmissionStatus.REVISION_REQUIRED
                last_submission.save()
                due_date = form.cleaned_data['due_date']

                feedback = Feedback.objects.create(
                    submission_field=last_submission)
                feedback.file = request.FILES['feedback_file']
                feedback.description = feedback_description
                feedback.save()

                # Create a new submission with the provided due date
                new_submission = Submission.objects.create(
                    internship=internship, due_date=due_date, status=SubmissionStatus.PENDING)
                Notification.create_notification(
                    title="New Submitted Feedback",
                    content=f"Student {str(self.request.user)} has submitted a new feedback for {internship.course}.",
                    receiver=internship.student,
                )
            else:
                return self.get(request, *args, **kwargs)

        elif action == 'extend':
            # handle the extend action here
            if form.is_valid():
                due_date = form.cleaned_data['due_date']
                last_submission = internship.submissions.latest(
                    'creation_date')
                last_submission.due_date = due_date
                last_submission.save()
                Notification.create_notification(
                        title="New Due Date",
                        content=f"Instructor {str(self.request.user)} has submitted a new due date for {internship.student.department.code}{internship.course} at {due_date}.",
                        receiver=internship.student,
                )
            else:
                return self.get(request, *args, **kwargs)

        elif action == 'submission_upload' and report_form.is_valid():
            existing_report = Submission.objects.filter(
                internship=internship, status=SubmissionStatus.PENDING).first()

            if existing_report and timezone.now() <= existing_report.due_date:
                existing_report.file = report_form.cleaned_data['file']
                existing_report.creation_date = timezone.now()
                existing_report.save()
        Notification.create_notification(
            title="New Submitted Report",
            content=f"Student {str(self.request.user)} has submitted a new report for {internship.student.department.code} {internship.course}.",
            receiver=internship.instructor,
        )
        return redirect('reports:view_internships')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExtensionForm()
        context['report_form'] = StudentReportForm()
        submissions = self.get_object().submissions.all()
        context['submissions'] = submissions.order_by('-id')
        context['last_submission'] = submissions.last()
        context['submission_set'] = self.get_object().submissions.exists()
        context['now'] = timezone.now()
        context['action'] = self.request.POST.get('action')
        return context

# class StatisticsDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
