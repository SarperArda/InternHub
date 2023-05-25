from django.db import models
from users.models import EngineeringDepartment, User, Course, Student, Instructor
from django.core.validators import FileExtensionValidator
import random
from django.core.validators import MinValueValidator, MaxValueValidator
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

    def __str__(self):
        return self.name.title()


class CompanyRequest(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null= True, related_name='+')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, related_name='+')


class CompanyRelatedDemand(models.Model):
    demand_date = models.DateTimeField(auto_now_add=True, null=True)
    description = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True


class CompanyApprovalValidationApplication(CompanyRelatedDemand):
    course = models.ForeignKey(Course, blank=True, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='company-approval-demands',
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    requested_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='+')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='cava_applications')

class EvaluationByStudent(CompanyRelatedDemand):
    grade = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

class CAVAManager:
    @staticmethod
    def create_CAVAs():
        students = Student.objects.all()
        student_count = students.count()
        companies = Company.objects.all()
        companies_count = companies.count()
        for i in range(0, 2 * student_count):
            number = random.randint(0, companies_count - 1)
            if i % 2 == 0:
                pk = 1
            else:
                pk = 2
            cava = CompanyApprovalValidationApplication(course=Course.objects.get(pk=pk),
                 file='uploads/empty.pdf', status='APPROVED', student=students[i//2],
                                                    requested_company=companies[number])
            print(students[i//2].first_name + students[i//2].last_name)
            cava.save()

