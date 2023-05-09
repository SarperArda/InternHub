from django.db import models
from users.models import EngineeringDepartments
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    field = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    departments = models.CharField(max_length=50, null=True, blank=True)




class CompanyRelatedDemand(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, related_name='company')
    file = models.FileField(upload_to='uploads/', null=True)
    demand_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, null=True)


class CompanyRequest(CompanyRelatedDemand):
    status = models.TextChoices('status', 'PENDING ACCEPTED REJECTED')


class CompanyApprovalValidationApplication(CompanyRelatedDemand):
    status = models.TextChoices('status', 'PENDING ACCEPTED REJECTED')


class EvaluationByStudent(CompanyRelatedDemand):
    grade = models.IntegerField(null=True)
