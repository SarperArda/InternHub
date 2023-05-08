from django.db import models
from main.models import User
from main.models import EngineeringDepartments
from student.models import Student
from chair.models import Chair
from instructor.models import Instructor
from departmentSecretary.models import DepartmentSecretary


class Dean(User):
    is_staff = True
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)
    chairs = models.ManyToManyField(Chair, blank=True, editable=False,
                                        related_name='dean_of_chairs')
    secretaries = models.ManyToManyField(DepartmentSecretary, blank=True, editable=False,
                                        related_name='dean_of_secretaries')
    instructors = models.ManyToManyField(Instructor, blank=True, editable=False,
                                        related_name='dean_of_instructors')
    students = models.ManyToManyField(Student, blank=True, editable=False,
                                        related_name='dean_of_students')

    def add_student(self, student):
        self.students.add(student)

    def add_instructor(self, instructor):
        self.instructors.add(instructor)

    def add_secretary(self, secretary):
        self.secretaries.add(secretary)

    def add_chair(self, chair):
        self.chairs.add(chair)

    def remove_secretary(self, secretary):
        self.secretaries.remove(secretary)

    def remove_instructor(self, instructor):
        self.instructors.remove(instructor)

    def remove_student(self, student):
        self.students.remove(student)

    def remove_chair(self, chair):
        self.chairs.remove(chair)

    def get_all_student(self):
        return self.students

    def get_all_instructors(self):
        return self.instructors

    def get_all_secretaries(self):
        return self.secretaries

    def get_all_chairs(self):
        return self.chairs

    def remove_dean_association(self, user):
        if isinstance(user, Student):
            self.remove_student(user)
        elif isinstance(user, Instructor):
            self.remove_instructor(user)
        elif isinstance(user, DepartmentSecretary):
            self.remove_secretary(user)
        elif isinstance(user, Chair):
            self.remove_chair(user)

    def add_dean_association(self, user):
        if isinstance(user, Student):
            self.add_student(user)
        elif isinstance(user, Instructor):
            self.add_instructor(user)
        elif isinstance(user, DepartmentSecretary):
            self.add_secretary(user)
        elif isinstance(user, Chair):
            self.add_chair(user)

    @staticmethod
    def update_dean_association(is_add, user):
        try:
            dean = Dean.objects.all()[0]
            if is_add:
                dean.add_dean_association(user)
            else:
                dean.remove_dean_association(user)

        except():
            dean = None

    class Meta:
        verbose_name = 'Dean'
        verbose_name_plural = 'Deans'

# Create your models here.
