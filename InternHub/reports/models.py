from django.db import models
from users.models import Student, Course, Instructor
from company.models import Company, CompanyApprovalValidationApplication, EvaluationByStudent
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

yes_no_choices = ('Yes', 'Yes'), ('No', 'No')
satisfactory_choices = ('Satisfactory', 'Satisfactory'), ('Revision Required',
                                                          'Revision Required'), ('Unsatisfactory', 'Unsatisfactory')


class Status(models.TextChoices):
    PENDING = 'PE', 'Pending'
    ACCEPTED = 'AC', 'Accepted'
    REJECTED = 'RE', 'Rejected'

class SubmissionStatus(models.TextChoices):
    SATISFACTORY = 'SA', 'Satisfactory',
    REVISION_REQUIRED = 'RR', 'Revision Required',
    UNSATISFACTORY = 'UN', 'Unsatisfactory',
    PENDING = 'PE', 'Pending'


class Task(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    description = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='uploads/', null=True)


class Submission(Task):
    status = models.CharField(
        max_length=2,
        choices=SubmissionStatus.choices,
        default=Status.PENDING,
    )
    due_date = models.DateTimeField()


class Feedback(Task):
    submission_field = models.OneToOneField(
        Submission, on_delete=models.CASCADE, null=True, related_name='feedback')


class FormModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    submission_date = models.DateTimeField(auto_now=True, editable=False)
    description = models.CharField(max_length=100, null=True)


class ConfidentialCompany(models.Model):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    company_name = models.CharField(max_length=100)
    is_work_related = models.CharField(max_length=3, choices=yes_no_choices)
    supervisor_background = models.CharField(
        max_length=3, choices=yes_no_choices)


class WorkAndReportEvaluation(models.Model):
    grade_of_performing_work = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    grade_of_solving_engineering_problems = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    grade_of_recognizing_ethics = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    grade_of_acquiring_knowledge = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                       blank=True, null=True)
    grade_of_applying_knowledge = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                      blank=True, null=True)
    grade_of_has_awareness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                 blank=True, null=True)
    grade_of_making_judgements = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                     blank=True, null=True)
    grade_of_preparing_reports = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                                     blank=True, null=True)

    exp_is_able_to_perform_work = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_able_to_solve_engineering_problems = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_recognize_ethics = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_able_to_acquire_knowledge = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_able_to_apply_new_knowledge = models.CharField(
        max_length=100, blank=True, null=True)
    exp_has_awareness = models.CharField(max_length=100, blank=True, null=True)
    exp_is_make_informed_judgments = models.CharField(
        max_length=100, blank=True, null=True)
    exp_is_able_to_prepare_reports = models.CharField(
        max_length=100, blank=True, null=True)


class Internship(models.Model):
    # Models
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, related_name='internship')
    instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, related_name='internship', default=None)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, related_name='internship')
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name='internship')

    # Forms
    work_and_report_evaluation_form = models.OneToOneField(WorkAndReportEvaluation, on_delete=models.SET_NULL,
                                                           null=True, related_name='internship', default=None)
    confidential_company_form = models.OneToOneField(
        ConfidentialCompany, on_delete=models.SET_NULL, null=True, related_name='internship', default=None)

    # Current status of the internship
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # Company Related Demands
    company_approval = models.OneToOneField(
        CompanyApprovalValidationApplication, on_delete=models.SET_NULL, null=True, related_name='internship')
    company_evaluation = models.OneToOneField(
        EvaluationByStudent, on_delete=models.SET_NULL, null=True, related_name='internship', default=None)

    # Student Report
    student_report = models.OneToOneField(
        Submission, on_delete=models.SET_NULL, null=True, related_name='internship', default=None)

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name + "'s " + self.course.name + " Course"

class StudentReport(models.Model):
    report = models.FileField(upload_to='reports/', null=True)


class InstructorFeedback(models.Model):
    feedback = models.FileField(upload_to='feedbacks/', null=True)

class InternshipManager:
    @staticmethod
    def create_internships():
        cavas = CompanyApprovalValidationApplication.objects.all()
        for cava in cavas:
            internship = Internship(student=cava.student, course=cava.course, company=cava.requested_company,
                                    company_approval=cava)
            internship.save()
    @staticmethod
    def list_instructors():
        for internship in Internship.objects.all():
            print("Internship name: " , internship, "Instructor name: " , internship.instructor)
