from django.db import models
from main.models import User
from main.models import EngineeringDepartments
from student.models import Student
from instructor.models import Instructor

# Create your models here.


class DepartmentSecretary(User):
    is_staff = True
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)
    instructors = models.ManyToManyField(Instructor, blank=True, editable=False,
                                        related_name= 'secretary_of_instructor')
    students = models.ManyToManyField(Student, blank=True, editable=False,
                                        related_name= 'secretary_of_students')

    def add_student(self, student):
        self.students.add(student)

    def add_instructor(self, instructor):
        self.instructors.add(instructor)

    def remove_student(self, student):
        self.students.remove(student)

    def remove_instructor(self, instructor):
        self.students.remove(instructor)

    def get_students_of_department(self):
        return self.students

    def get_instructors_of_department(self):
        return self.instructors

    def remove_secretary_association(self, user):
        if isinstance(user, Student):
            self.remove_student(user)
        elif isinstance(user, Instructor):
            self.remove_instructor(user)

    def add_secretary_association(self, user):
        if isinstance(user, Student):
            self.add_student(user)
        elif isinstance(user, Instructor):
            self.add_instructor(user)

    @staticmethod
    def update_department_secretary_association(is_add, user):
        secretary = DepartmentSecretary.objects.get(department=user.department)
        if is_add:
            secretary.add_secretary_association(user)
        else:
            secretary.remove_secretary_association(user)

    class Meta:
        verbose_name = 'Department Secretary'
        verbose_name_plural = 'Department Secretaries'

