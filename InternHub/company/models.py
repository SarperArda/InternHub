from django.db import models
from users.models import EngineeringDepartment, User
# Create your models here.
STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

class Company(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    field = models.CharField(max_length=100, null=True)
    departments = models.ManyToManyField(EngineeringDepartment, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', null=True)



class CompanyRequest(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null= True, related_name='+')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='+')


class CompanyRelatedDemand(models.Model):
    demand_date = models.DateTimeField(auto_now_add=True, null=True)
    description = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True


class CompanyApprovalValidationApplication(CompanyRelatedDemand):
    file = models.FileField(upload_to='company-approval-demands', null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')


class EvaluationByStudent(CompanyRelatedDemand):
    grade = models.IntegerField(null=True)
