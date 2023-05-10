from django.db import models
from users.models import EngineeringDepartment
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    field = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    departments = models.ManyToManyField(EngineeringDepartment, blank=True)

    def __str__(self):
        return self.name.title()


class CompanyRelatedDemand(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name='company')
    file = models.FileField(upload_to='company-related-demands', null=True)
    demand_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, null=True)


class CompanyRequest(CompanyRelatedDemand):
    status = models.TextChoices('status', 'PENDING ACCEPTED REJECTED')


class CompanyApprovalValidationApplication(CompanyRelatedDemand):
    status = models.TextChoices('status', 'PENDING ACCEPTED REJECTED')


class EvaluationByStudent(CompanyRelatedDemand):
    grade = models.IntegerField(null=True)
