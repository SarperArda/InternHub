from django.db import models
from users.models import Student, Course, Instructor
from company.models import Company, CompanyApprovalValidationApplication, EvaluationByStudent
# Create your models here.


class Status(models.TextChoices):
    PENDING = 'PE', 'Pending'
    ACCEPTED = 'AC', 'Accepted'
    REJECTED = 'RE', 'Rejected'


class Task(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='uploads/', null=True)


class Submission(Task):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )


class Feedback(Task):
    submission_field = models.OneToOneField(
        Submission, on_delete=models.CASCADE, null=True, related_name='feedback')


class Form(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    submission_date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=100, null=True)


class GradingForm(Form):
    due_date = models.DateTimeField(null=True)
    student_submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE, null=True, related_name='grading_form')
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )


class ConfidentialCompanyForm(Form):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )


class EvaluationForm(Form):
    grade = models.IntegerField(null=True)
    is_work_related = models.BooleanField(null=True)
    supervisor_background = models.BooleanField(null=True)


class Internship(models.Model):
    # Models
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, related_name='internship')
    instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, related_name='internship')
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, related_name='internship')
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name='internship')

    # Forms
    grading_form = models.OneToOneField(
        GradingForm, on_delete=models.SET_NULL, null=True, related_name='internship')
    evaluation_form = models.OneToOneField(
        EvaluationForm, on_delete=models.SET_NULL, null=True, related_name='internship')
    confidential_company_form = models.OneToOneField(
        ConfidentialCompanyForm, on_delete=models.SET_NULL, null=True, related_name='internship')

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
        EvaluationByStudent, on_delete=models.SET_NULL, null=True, related_name='internship')
