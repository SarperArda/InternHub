from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import CompanyForm, CAVAForm, CompanyEvaluationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from .models import Company, CompanyRequest, CompanyApprovalValidationApplication
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from users.decorators import allowed_users
from django.utils import timezone
from reports.models import Internship, Status
from users.models import Student, User, DepartmentSecretary
from django.core.exceptions import ValidationError
from users.views import RoleRequiredMixin, UserRequiredMixin
from announcements.models import Notification
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.views import View
from django.http import FileResponse
from reports.models import SubmissionStatus
import io
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.


class CreateCompanyRequestView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'company/create-company-request.html'
    form_class = CompanyForm
    success_url = reverse_lazy('company:companies')
    allowed_roles = ['STUDENT']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

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

class CompanyAddView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'company/company-add.html'
    form_class = CompanyForm
    success_url = reverse_lazy('company:companies')
    allowed_roles = ['DEPARTMENT_SECRETARY']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

    def form_valid(self, form):
        company = form.save(commit=False)
        company.status = 'APPROVED'

        company.save()
        form.save_m2m()
        return super().form_valid(form)
    
class CompaniesView(LoginRequiredMixin, ListView):
    template_name = 'company/companies.html'
    model = Company
    context_object_name = 'companies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(status='APPROVED')


class ListCompanyRequestsView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'company/company-requests.html'
    model = CompanyRequest
    context_object_name = 'requests'
    ordering = 'id'
    allowed_roles = ['SUPERUSER', 'DEPARTMENT_SECRETARY']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context


class CompanyRequestDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = CompanyRequest
    template_name = 'company/request-detail.html'
    context_object_name = 'request'
    allowed_roles = ['SUPERUSER', 'DEPARTMENT_SECRETARY']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

    def form_valid(self, form):
        student = Student.objects.get(user_id=self.request.user.user_id)
        course = form.instance.course

        pending_internship = Internship.objects.filter(
            student=student,
            course=course,
            status=Status.PENDING
        ).exists()

        if pending_internship:
            form.add_error(None, "You have a pending internship for this course. You cannot submit another CAVA.")
            return self.form_invalid(form)

        cava = form.save(commit=False)
        cava.status = 'PENDING'
        cava.student = student
        cava.demand_date = timezone.now()

        department_secretary = User.objects.get(department=student.department, role='DEPARTMENT_SECRETARY')
        Notification.create_notification(
            title="CAVA Request Submitted",
            content=f'Student { student.first_name } { student.last_name } has submitted a CAVA request.'
            ' Please review the details in your dashboard. Thank you.',
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

    def get_queryset(self):
        return CompanyApprovalValidationApplication.objects.filter(status='PENDING')


class CAVADetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    template_name = 'company/cava-request-detail.html'
    model = CompanyApprovalValidationApplication
    context_object_name = 'request'
    allowed_roles = ['SUPERUSER', 'DEPARTMENT_SECRETARY']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

    def post(self, request, *args, **kwargs):
        cava_request = self.get_object()
        action = request.POST.get('action')
        student = cava_request.student
        # Todo Send notification
        if action == 'approve':
            cava_request.status = 'APPROVED'
           
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
class CompanyEvaluationView(LoginRequiredMixin, UserRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'company/evaluate-company.html'
    form_class = CompanyEvaluationForm
    success_url = reverse_lazy('main:home')
    allowed_roles = ['STUDENT']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

    def get_queryset(self):
        student = Student.objects.get(user_id=self.request.user.user_id)
        return self.model.objects.filter(student=student)

def generate_pdf(request, pk):
    internship_pk = pk
    print(internship_pk)
    c = canvas.Canvas('uploads/output.pdf', pagesize=letter)
    internship = Internship.objects.all().get(pk=internship_pk)

    def write_left_aligned_text(text, height, name, size):
        c.setFont(name, size)
        c.drawString(0.5 * inch, letter[1] - height * 0.3 * inch, text)

    def write_center_aligned_text(text, height, name, size):
        c.setFont(name, size)
        text_width = c.stringWidth(text, name, size)
        center = (letter[0] - text_width) / 2
        c.drawString(center, letter[1] - height * 0.3 * inch, text)

    def write_underlined_left_aligned_text(text, height, name, size):
        write_left_aligned_text(text, height, name, size)
        underline_y = letter[1] - 0.3 * height * inch - 0.29 * size
        text_width = c.stringWidth(text, name, size)
        c.setLineWidth(0.5)
        c.line(0.5 * inch, underline_y, 0.5 * inch + text_width, underline_y)

    def write_underlined_center_aligned_text(text, height, name, size):
        c.setFont(name, size)
        write_center_aligned_text(text, height, name, size)
        underline_y = letter[1] - height * 0.3 * inch - 0.29 * size
        text_width = c.stringWidth(text, name, size)
        center = (letter[0] - text_width) / 2
        c.setLineWidth(0.5)
        c.line(center, underline_y, center + text_width, underline_y)

    def draw_header(k, departmentName):
        logo_path = "users/static/img/logo.png"

        logo_x = 0.5 * inch
        logo_y = 9.5 * inch
        logo_width = 1.5 * inch
        logo_height = 1.5 * inch

        c.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)

        # Get the width of the text
        # insert var
        texts = ['Bilkent University', 'Engineering Faculty', departmentName]

        for text in texts:
            write_center_aligned_text(text, k, 'Helvetica-Bold', 14)
            k += 1

    department_name = internship.student.department.name
    draw_header(1, department_name)
    k = 5
    # New line
    write_center_aligned_text('Summer Training Grading Form', k, 'Helvetica-Bold', 14)
    # New line
    k = k + 1
    write_underlined_center_aligned_text('Confidential', k, 'Helvetica-Bold', 14)

    k = k + 1
    name = internship.student.first_name + internship.student.last_name
    write_left_aligned_text("Name - Surname: " + name, k, 'Helvetica-Bold', 14)

    k = k + 1
    name = internship.company.name
    write_left_aligned_text("Company Name: " + name, k, 'Helvetica-Bold', 14)

    k = k + 1
    name = internship.student.department.code + internship.course.code
    write_left_aligned_text("Course: " + name, k, 'Helvetica-Bold', 14)

    k = k + 1
    write_underlined_left_aligned_text("Part A: Work Place", k, 'Helvetica-Bold', 14)

    c.rect(0.5 * inch, letter[1] - 0.3 * (k + 5.0) * inch, letter[0] - 1 * inch, 1.7 * inch)

    k = k + 1
    if internship.confidential_company_form is None:
        confidential_grade = "No Data"
        answer1 = "No Data "
        answer2 = "No Data"
    else:
        conf = internship.confidential_company_form
        confidential_grade = conf.grade
        answer1 = conf.is_work_related
        answer2 = conf.supervisor_background

    write_left_aligned_text("Average of the grades on the Summer Training Evaluation form: " + str(confidential_grade),
                            k, 'Helvetica', 14)
    k = k + 1
    write_left_aligned_text("Is the work done related to computer engineering [Y/N]: " + str(answer1),
                            k, 'Helvetica', 14)
    k = k + 1
    write_left_aligned_text("Is the supervisor related to" + department_name + " or has a similar ",
                            k, 'Helvetica', 14)
    k = k + 1
    write_left_aligned_text("background: [Y/N]: " + str(answer2), k, 'Helvetica', 14)

    c.rect(0.5 * inch, letter[1] - 0.3 * (k + 7.0) * inch, letter[0] - 1 * inch, 1.4 * inch)

    status = internship.get_status_display()

    k = k + 3
    write_underlined_left_aligned_text("Part B: Report", k, 'Helvetica-Bold', 14)

    k = k + 1
    write_left_aligned_text("Report Status: " + status, k, 'Helvetica-Bold', 14)

    last_submission = internship.submissions.order_by('id').first()
    if last_submission is None:
        due_date = "No Data"
    else:
        due_date = last_submission.due_date.strftime('%Y-%m-%d')

    k = k + 2
    write_left_aligned_text("The most recent due date is: " + due_date, k, 'Helvetica-Bold', 14)

    c.rect(0.5 * inch, letter[1] - 0.3 * (k + 8.7) * inch, letter[0] - 1 * inch, 2.0 * inch)
    k = k + 3
    write_underlined_left_aligned_text("Part C: Final Version of The Report", k, 'Helvetica-Bold', 14)

    k = k + 1
    if internship.instructor is not None:
        instructor = internship.instructor.first_name + internship.instructor.last_name
    else:
        instructor = "No Data"

    write_left_aligned_text("Based on the Work Report Evaluation Given by: " + instructor, k, 'Helvetica', 14)

    k = k + 1
    wre = internship.work_and_report_evaluation_form
    if wre:
        if not wre.calculate_total_grade():
            work_grade = "No Data"
            items_grade = "No Data"
            report_grade = "No Data"
            awareness_grade = "No Data"
            ethics_grade = "No Data"
            app_grade = "No Data"
            acq_grade = "No Data"
            judge_grade = "No Data"
            solving_grade = "No Data"
            report_exp = "No Data"
            awareness_exp = "No Data"
            recognize_ethics = "No Data"
            acq_exp = "No Data"
            exp_judge = "No Data"
            exp_app = "No Data"
            exp_solve = "No Data"
            exp_work = "No Data"
        else:
            if wre.grade_of_preparing_reports:
                report_grade = wre.grade_of_preparing_reports
            else:
                report_grade = "No Data"
            if wre.grade_of_performing_work:
                work_grade = wre.grade_of_performing_work
            else:
                work_grade = "None"
            items_grade = wre.calculate_total_grade()
            if report_grade != "No Data":
                items_grade = items_grade - report_grade
            if work_grade != "No Data":
                items_grade = items_grade - work_grade
            if wre.grade_of_has_awareness:
                awareness_grade = wre.grade_of_has_awareness
            else:
                awareness_grade = "No Data"
            if wre.grade_of_recognizing_ethics:
                ethics_grade = wre.grade_of_recognizing_ethics
            else:
                ethics_grade = "No Data"
            if wre.grade_of_applying_knowledge:
                app_grade = wre.grade_of_applying_knowledge
            else:
                app_grade = "No Data"
            if wre.grade_of_acquiring_knowledge:
                acq_grade = wre.grade_of_acquiring_knowledge
            else:
                acq_grade = "No Data"
            if wre.grade_of_making_judgements:
                judge_grade = wre.grade_of_making_judgements
            else:
                judge_grade = "No Data"
            if wre.grade_of_solving_engineering_problems:
                solving_grade = wre.grade_of_solving_engineering_problems
            else:
                solving_grade = "No Data"
        if wre.exp_is_able_to_prepare_reports:
            report_exp = wre.exp_is_able_to_prepare_reports
        else:
            report_exp = "No Data"
        if wre.exp_has_awareness:
            awareness_exp = wre.exp_has_awareness
        else:
            awareness_exp = "No Data"
        if wre.exp_is_recognize_ethics:
            recognize_ethics = wre.exp_is_recognize_ethics
        else:
            recognize_ethics = "No Data"
        if wre.exp_is_able_to_acquire_knowledge:
            acq_exp = wre.exp_is_able_to_acquire_knowledge
        else:
            acq_exp = "No Data"
        if wre.exp_is_make_informed_judgments:
            exp_judge = wre.exp_is_make_informed_judgments
        else:
            exp_judge = "No Data"
        if wre.exp_is_able_to_apply_new_knowledge:
            exp_app = wre.exp_is_able_to_apply_new_knowledge
        else:
            exp_app = "No Data"
        if wre.exp_is_able_to_solve_engineering_problems:
            exp_solve = wre.exp_is_able_to_solve_engineering_problems
        else:
            exp_solve = "No Data"
        if wre.exp_is_able_to_perform_work:
            exp_work = wre.exp_is_able_to_perform_work
        else:
            exp_work = "No Data"
    else:
        work_grade = "No Data"
        items_grade = "No Data"
        report_grade = "No Data"
        awareness_grade = "No Data"
        ethics_grade = "No Data"
        app_grade = "No Data"
        acq_grade = "No Data"
        judge_grade = "No Data"
        solving_grade = "No Data"
        report_exp = "No Data"
        awareness_exp = "No Data"
        recognize_ethics = "No Data"
        acq_exp = "No Data"
        exp_judge = "No Data"
        exp_app = "No Data"
        exp_solve = "No Data"
        exp_work = "No Data"

    write_left_aligned_text("Assessment Quality Score of the Work - item(1): " + str(work_grade), k, 'Helvetica', 14)

    k = k + 1
    write_left_aligned_text("Assessment Quality Score of the Work - items(2)-(7): " + str(items_grade), k, 'Helvetica',
                            14)

    k = k + 1
    write_left_aligned_text("Assessment Quality Score of the Evaluation of the Report: " + str(report_grade), k,
                            'Helvetica', 14)

    k = k + 4
    write_underlined_left_aligned_text("Overall Evaluation: " + status, k, 'Helvetica-Bold', 14)

    k = k + 1
    write_left_aligned_text("Evaluator: ", k, 'Helvetica-Bold', 14)
    write_center_aligned_text("Name - Surname: " + instructor, k, 'Helvetica-Bold', 14)

    k = k + 1
    write_left_aligned_text("Signature: ", k, 'Helvetica-Bold', 14)
    c.drawString(3.5 * inch, letter[1] - k * 0.3 * inch, "Date: " + due_date)

    c.showPage()

    draw_header(1, department_name)
    # New line
    k = 5
    write_center_aligned_text('Work And Report Evaluation Form', k, 'Helvetica-Bold', 14)

    for i in range(0, 9):
        for j in range(0, 3):
            c.rect(0.5 * inch, letter[1] - 0.3 * (k + 7.0 + i * 3) * inch, 4 * inch, 0.9 * inch)
            c.rect(4.5 * inch, letter[1] - 0.3 * (k + 7.0 + i * 3) * inch, 2 * inch, 0.9 * inch)
            c.rect(6.5 * inch, letter[1] - 0.3 * (k + 7.0 + i * 3) * inch, 1.5 * inch, 0.9 * inch)

    write_left_aligned_text('Able to perform a work at the level expected',
                            12.6, 'Helvetica', 12)
    write_left_aligned_text('from a summer training in the area of department',
                            13.8, 'Helvetica', 12)
    write_left_aligned_text('Solves complex engineering problems by applying',
                            15.6, 'Helvetica', 12)
    write_left_aligned_text('principles of engineering, science and mathematics',
                            16.8, 'Helvetica', 12)
    write_left_aligned_text('Solves complex engineering problems by applying',
                            15.6, 'Helvetica', 12)
    write_left_aligned_text('principles of engineering, science and mathematics',
                            16.8, 'Helvetica', 12)
    write_left_aligned_text('Recognizes ethical and professional responsibilities',
                            18.6, 'Helvetica', 12)
    write_left_aligned_text('in engineering situations',
                            19.8, 'Helvetica', 12)
    write_left_aligned_text('Able to make informed judgments that consider the ',
                            21.6, 'Helvetica', 12)
    write_left_aligned_text('impact of solutions in global, environmental, societal',
                            22.8, 'Helvetica', 12)
    write_left_aligned_text('and economic context',
                            23.7, 'Helvetica', 12)
    write_left_aligned_text('Able to acquire new knowledge using',
                            24.6, 'Helvetica', 12)
    write_left_aligned_text('appropriate learning strategies',
                            25.8, 'Helvetica', 12)
    write_left_aligned_text('Able to apply acquired knowledge as needed',
                            28.2, 'Helvetica', 12)
    write_left_aligned_text('Has awareness about diversity, equity and inclusion',
                            30.9, 'Helvetica', 12)
    write_left_aligned_text('Able to prepare reports with high standards in terms of',
                            33.9, 'Helvetica', 12)
    write_left_aligned_text('content, organization and style',
                            35.1, 'Helvetica', 12)
    c.setFont('Helvetica', 12)
    c.drawString(4.6 * inch, letter[1] - 3.2 * inch, "Pages on which: ")
    c.drawString(4.6 * inch, letter[1] - 3.4 * inch, "evidence is found: ")
    c.drawString(6.6 * inch, letter[1] - 3.3 * inch, "Grade given: ")
    c.drawString(4.6 * inch, letter[1] - 4.2 * inch, exp_work)
    c.drawString(4.6 * inch, letter[1] - 5.1 * inch, exp_solve)
    c.drawString(4.6 * inch, letter[1] - 6 * inch, recognize_ethics)
    c.drawString(4.6 * inch, letter[1] - 6.9 * inch, exp_judge)
    c.drawString(4.6 * inch, letter[1] - 7.8 * inch, acq_exp)
    c.drawString(4.6 * inch, letter[1] - 8.7 * inch, exp_app)
    c.drawString(4.6 * inch, letter[1] - 9.5 * inch, awareness_exp)
    c.drawString(4.6 * inch, letter[1] - 10.4 * inch, report_exp)
    c.drawString(7.1 * inch, letter[1] - 4.2 * inch, str(work_grade))
    c.drawString(7.1 * inch, letter[1] - 5.1 * inch, str(solving_grade))
    c.drawString(7.1 * inch, letter[1] - 6 * inch, str(judge_grade))
    c.drawString(7.1 * inch, letter[1] - 6.9 * inch, str(ethics_grade))
    c.drawString(7.1 * inch, letter[1] - 7.8 * inch, str(acq_grade))
    c.drawString(7.1 * inch, letter[1] - 8.7 * inch, str(app_grade))
    c.drawString(7.1 * inch, letter[1] - 9.5 * inch, str(awareness_grade))
    c.drawString(7.1 * inch, letter[1] - 10.4 * inch, str(report_grade))

    c.save()
    return FileResponse(open('uploads/output.pdf', 'rb'), as_attachment=True, filename=internship.__str__())


