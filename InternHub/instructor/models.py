from django.db import models
from main.models import User
from main.models import EngineeringDepartments
from student.models import Student
class Instructor(User):
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)
    students = models.ManyToManyField(Student, blank=True, editable=False,
                                            related_name='instructor_of_student')

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def assign_students_to_instructor(self, student):
        self.students.add(student)

    def remove_students_to_instructor(self, student):
        self.students.remove(student)

# Create your models here.
