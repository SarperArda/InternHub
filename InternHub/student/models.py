from django.db import models
from main.models import User
from main.models import EngineeringDepartments
from main.models import Courses

class Student(User):
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)
    course = models.CharField(max_length=6, choices=Courses.choices, null=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

# Create your models here.
