from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, UpdateView, CreateView, View
from django.views.generic.base import TemplateView
from reports.forms import ConfidentialCompanyForm
from reports.forms import SummerTrainingGradingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WorkAndReportEvaluationForm, InternshipAssignmentForm
from .models import Internship,Feedback, ConfidentialCompany,Statistic
from .forms import WorkAndReportEvaluationForm, ExtensionForm
from .forms import StudentReportForm
from .forms import FeedbackForm
from users.models import Student
from .models import StudentReport, WorkAndReportEvaluation, Submission, InstructorFeedback, ExtensionRequest
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
from InternHub.manager import StatisticManager
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
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        if Internship.objects.filter(id = internship_id).exists():
            internship = Internship.objects.get(id = internship_id)
            context['student_name'] = internship.student.first_name + " " + internship.student.last_name
            context['department'] = internship.student.department.name
            context['instructor_name'] = internship.instructor.first_name + " " + internship.instructor.last_name
            context['course'] = internship.student.department.code + " " + internship.course.code
        return context


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
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
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
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
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



class ReportsView(ListView):
    model = StudentReport
    template_name = 'reports/view_reports.html'
    context_object_name = 'reports'

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
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
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
                instructor = instructors[instructor_index]
                internship.instructor = instructor
                internship.save()

                # Increment instructor index and loop back if needed
                instructor_index += 1
                if instructor_index >= instructor_count:
                    instructor_index = 0
                Notification.create_notification(
                        title="New Internship Assignment",
                        content=f"Secretary {str(self.request.user)} has assigned a new instructor {str(internship.instructor)} for {internship.student.department.code}{internship.course}.",
                        receiver=internship.student,
                )

                Notification.create_notification(
                        title="New Internship Assignment",
                        content=f"Secretary {str(self.request.user)} has assigned a new student {str(internship.student)} for {internship.student.department.code}{internship.course}.",
                        receiver=internship.instructor,
                )

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
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True

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
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'Unsatisfactory':
            internship_id = request.POST.get('internship_id')
            internship = Internship.objects.get(pk=internship_id)
            internship.status = SubmissionStatus.UNSATISFACTORY
            internship.save()
            Notification.create_notification(
                        title="Unsatisfactory Internship",
                        content=f"Your internship {internship.student.department.code}{internship.course} has been marked as unsatisfactory by {str(self.request.user)}.",
                        receiver=internship.student,
            )
        elif action == 'Extend': 
            form = ExtensionForm(request.POST)
            if form.is_valid():
                due_date = form.cleaned_data['extension_date']
                internships = self.get_queryset().filter(status=SubmissionStatus.PENDING)
                for internship in internships:
                    # Get the existing submission with status "PENDING"
                    report = internship.submissions.filter(
                        status=SubmissionStatus.PENDING).first()
                    # Create a new submission if it doesn't exist
                    if report is None:
                        report = Submission.objects.create(
                            internship=internship, due_date=due_date)
                        Notification.create_notification(
                            title="New Submission",
                            content=f"Instructor {str(self.request.user)} has assigned a new submission for {internship.student.department.code}{internship.course}.",
                            receiver=internship.student,
                        )
                    else:
                        Notification.create_notification(
                            title="New Due Date",
                            content=f"Instructor {str(self.request.user)} has submitted a new due date for {internship.student.department.code}{internship.course} at {due_date}.",
                            receiver=internship.student,
                        )
                        report.due_date = due_date
                        report.save()
                    # Add the submission to the internship if it doesn't exist
                    if report.id is None:
                        internship.submissions.add(report)

                    
                # Redirect to the view page
                return redirect('reports:view_internships')

        # Re-render the page with the same context if form is not valid
            return self.get(request, *args, **kwargs)
        return redirect('reports:view_internships')


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
        if action == 'extend':
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
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

class ListSubmissionView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'reports/submissions_list.html'
    model = Internship
    context_object_name = 'internships'
    allowed_roles = ['INSTRUCTOR', 'DEPARTMENT_SECRETARY', 'STUDENT']

    def get_queryset(self):
        if self.request.user.role == 'STUDENT':
            return Internship.objects.filter(student__user_id=self.request.user.user_id).order_by('id')
        elif self.request.user.role == 'INSTRUCTOR':
            return Internship.objects.filter(instructor__user_id=self.request.user.user_id).order_by('id')
        else:  # if the user is a DEPARTMENT_SECRETARY
            return Internship.objects.filter(student__department=self.request.user.department).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        internships = self.get_queryset()
        context['internships'] = internships
        context['latest_submissions'] = {}
        context['feedback_needed'] = {}
        context['feedback_recieved'] = {}
        context['feedback_form'] = FeedbackForm()
        context['form'] = StudentReportForm()
        context['extension_form'] = ExtensionForm()
        context['date_passed'] = {}
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True

        for internship in internships:
            if internship.submissions.exists():
                context['latest_submissions'][internship.pk] = internship.submissions.order_by('-id').first()
                last_submission = internship.submissions.all().latest('id')
                submissions = internship.submissions.all().order_by('-id')
                second_last_submission = submissions[1] if submissions.count() > 1 else None 

                if last_submission.file == "" and second_last_submission is not None:
                    context['feedback_recieved'][internship.pk] = True                
                else:
                    context['feedback_recieved'][internship.pk] = False
                if last_submission.due_date < timezone.now():
                    context['date_passed'][internship.pk] = True
                # Check if feedback is needed for the last submission
                feedback_needed = bool(
                    last_submission.file.name) and last_submission.status == SubmissionStatus.PENDING
                context['feedback_needed'][internship.pk] = feedback_needed
            else:
                context['latest_submissions'][internship.pk] = None
                context['feedback_needed'][internship.pk] = False
        return context
    
    def post(self, request, *args, **kwargs):
        internship_id = request.POST.get('internship_id')
        internship = get_object_or_404(Internship, id=internship_id)
        latest_submission = internship.submissions.latest('id')
        action = request.POST.get('action')

        if action == 'extension_request':
            extension_form = ExtensionForm(request.POST)
            if extension_form.is_valid() and not hasattr(latest_submission, 'extension'):
                # Process the extension request
                date = extension_form.cleaned_data['extension_date']
                ExtensionRequest.objects.create(
                    submission=latest_submission, extension_date=date)
                Notification.create_notification(
                    title="Extension Request",
                    content=f"Student {str(self.request.user)} has requested an extension for {internship.student.department.code} {internship.course} at {date}.",
                    receiver=internship.instructor,
                )
                latest_submission.save()
        elif action == 'satisfactory':
            latest_submission.status = SubmissionStatus.SATISFACTORY
            internship.status = SubmissionStatus.SATISFACTORY
            latest_submission.save()
            internship.save()
            Notification.create_notification(
                title="Satisfactory Report",
                content=f"Your report for {internship.student.department.code} {internship.course} has been marked as satisfactory.",
                receiver=internship.student,
            )
        elif action == 'revision_required':
            feedback_form = FeedbackForm(request.POST, request.FILES)
            if feedback_form.is_valid():
                # Process the feedback upload
                feedback_description = feedback_form.cleaned_data['description']
                due_date = feedback_form.cleaned_data['due_date']

                # Update the status of the last submission to revision required
                last_submission = internship.submissions.latest('creation_date')
                last_submission.status = SubmissionStatus.REVISION_REQUIRED
                
                # Create a new feedback object and initialize it with the last submission
                feedback = Feedback.objects.create(
                    submission_field=last_submission)
                feedback.file = request.FILES['file']
                feedback.description = feedback_description

                feedback.save()
                last_submission.save()

                Notification.create_notification(
                    title="Revision Required",
                    content=f"Your report for {internship.student.department.code} {internship.course} has been marked as revision required.",
                    receiver=internship.student,
                )
                # Create a new submission with the provided due date
                new_submission = Submission.objects.create(
                    internship=internship, due_date=due_date, status=SubmissionStatus.PENDING)

        elif action == 'submit_report':
            form = StudentReportForm(request.POST, request.FILES)

            if form.is_valid():
                existing_report = Submission.objects.filter(
                    internship=internship, status=SubmissionStatus.PENDING).first()

                if existing_report and timezone.now() <= existing_report.due_date:
                    existing_report.file = form.cleaned_data['file']
                    existing_report.creation_date = timezone.now()
                    existing_report.save()

                    Notification.create_notification(
                        title="Report Submitted",
                        content=f"Your report for {internship.student.department.code} {internship.course} has been submitted.",
                        receiver=internship.student,
                    )

                    Notification.create_notification(
                        title="Report Submitted",
                        content=f"Student {str(self.request.user)} has submitted a report for {internship.student.department.code} {internship.course}.",
                        receiver=internship.instructor,
                    )
            
                # Handle the file upload and any other necessary logic
        elif action == 'approve_extension':
            latest_submission.due_date = latest_submission.extension.extension_date
            latest_submission.extension.delete()
            latest_submission.save()
            Notification.create_notification(
                title="Extension Approved",
                content=f"Your extension request for {internship.student.department.code} {internship.course} has been approved.",
                receiver=internship.student,
            )
        elif action == 'reject_extension':
            latest_submission.extension.delete()
            Notification.create_notification(
                title="Extension Rejected",
                content=f"Your extension request for {internship.student.department.code} {internship.course} has been rejected.",
                receiver=internship.student,
            )
        return redirect('reports:submission_list')
    
class ListFeedbackView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Feedback
    template_name = 'reports/feedback_list.html'
    context_object_name = 'feedbacks'
    allowed_roles = ['STUDENT', 'INSTRUCTOR']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context
    
    def get_queryset(self):
        if self.request.user.role == 'STUDENT':
            return Feedback.objects.filter(submission_field__internship__student__user_id=self.request.user.user_id).order_by('id')
        elif self.request.user.role == 'INSTRUCTOR':
            return Feedback.objects.filter(submission_field__internship__instructor__user_id=self.request.user.user_id).order_by('id')


# class StatisticsDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView)

class StatisticView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Statistic
    template_name = 'reports/statistics.html'
    context_object_name = 'statistic'
    allowed_roles = ['DEAN', 'CHAIR']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        statistic = Statistic.objects.get(id=self.kwargs['pk'])

        if user.role == 'CHAIR':
            context['chair_department'] = Statistic.objects.all().filter(department=user.department).first().pk
        if statistic.department.code == 'CS':
            context['cs'] = statistic.pk
            context['me'] = statistic.pk + 1
            context['ee'] = statistic.pk + 2
            context['ie'] = statistic.pk + 3
        if statistic.department.code == 'ME':
            context['me'] = statistic.pk
            context['cs'] = statistic.pk - 1
            context['ee'] = statistic.pk + 1
            context['ie'] = statistic.pk + 2
        if statistic.department.code == 'EEE':
            context['ee'] = statistic.pk
            context['cs'] = statistic.pk - 2
            context['me'] = statistic.pk - 1
            context['ie'] = statistic.pk + 1
        if statistic.department.code == 'IE':
            context['ie'] = statistic.pk
            context['cs'] = statistic.pk - 3
            context['me'] = statistic.pk - 2
            context['ee'] = statistic.pk - 1
    
        StatisticManager.update_statistics()
        if statistic.calculate_report_grade_average() is None:
            statistic.report_grade_average = 0
        if statistic.calculate_work_grade_average() is None:
            statistic.work_evaluation_grade_average = 0
        if statistic.calculate_company_evaluation_grade_average() is None:
            statistic.company_evaluation_grade_average = 0
        context['statistic'] = statistic
        return context
