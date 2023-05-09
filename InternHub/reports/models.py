from django.db import models
from users.models import Student
from company.models import Company, CompanyApprovalValidationApplication, EvaluationByStudent
# Create your models here.


class Task(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='uploads/', null=True)


class Submission(Task):
    status = models.TextChoices('status', 'PENDING ACCEPTED REJECTED')


class Feedback(Task):
    submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE, null=True)


class Form(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    submission_date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=100, null=True)


class GradingForm(Form):
    due_date = models.DateTimeField(null=True)
    student_submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE, null=True)
    status = models.TextChoices('status', 'PENDING ACCEPTED REJECTED')


class ConfidentialCompanyForm(Form):
    status = models.TextChoices('status', 'PENDING ACCEPTED REJECTED')


class EvaluationForm(Form):
    grade = models.IntegerField(null=True)


class Internship(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, related_name='internship')
    course = models.TextChoices('courser', '299', '399')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, related_name='company')
    grading_form = models.OneToOneField(
        GradingForm, on_delete=models.CASCADE, null=True, related_name='grading_form')
    evaluation_form = models.OneToOneField(
        EvaluationForm, on_delete=models.CASCADE, null=True, related_name='evaluation_form')
    confidential_company_form = models.OneToOneField(
        ConfidentialCompanyForm, on_delete=models.CASCADE, null=True, related_name='confidential_company_form')
    status = models.TextChoices(
        'status', 'PENDING SATISFACTORY UNSATISFACTORY')
    company_approval = models.OneToOneField(
        CompanyApprovalValidationApplication, on_delete=models.CASCADE, null=True, related_name='company_approval')
    company_evaluation = models.OneToOneField(
        EvaluationByStudent, on_delete=models.CASCADE, null=True, related_name='company_evaluation')
