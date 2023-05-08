from django.db import models
from main.models import User
from main.models import EngineeringDepartments
from student.models import Student
from instructor.models import Instructor
from departmentSecretary.models import DepartmentSecretary


class Chair(User):
    is_staff = True
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)
    students = models.ManyToManyField(Student, blank=True, editable=False,
                                      related_name='chair_of_students')
    secretary = models.OneToOneField(DepartmentSecretary, on_delete=models.SET_NULL, blank=True,
                                     null=True, related_name='chair_of_secretary')
    instructors = models.ManyToManyField(Instructor, blank=True, editable=False,
                                         related_name='chair_of_instructors')

    def add_student(self, student):
        self.students.add(student)

    def add_instructor(self, instructor):
        self.instructors.add(instructor)

    def add_secretary(self, secretary):
        self.secretary = secretary

    def remove_secretary(self):
        self.secretary.clear()

    def remove_instructor(self, instructor):
        self.instructors.remove(instructor)

    def remove_student(self, student):
        self.students.remove(student)

    def get_students_of_department(self):
        return self.students

    def get_instructors_of_department(self):
        return self.instructors

    def get_secretary_of_department(self):
        return self.secretary

    def remove_chair_association(self, user):
        if isinstance(user, Student):
            self.remove_student(user)
        elif isinstance(user, Instructor):
            self.remove_instructor(user)
        elif isinstance(user, DepartmentSecretary):
            self.remove_secretary()

    def add_chair_association(self, user):
        if isinstance(user, Student):
            self.add_student(user)
        elif isinstance(user, Instructor):
            self.add_instructor(user)
        elif isinstance(user, DepartmentSecretary):
            self.add_secretary(user)

    @staticmethod
    def update_chair_association(is_add, user):
        try:
            chair = Chair.objects.get(department=user.department)
            if is_add:
                chair.add_chair_association(user)
            else:
                chair.remove_chair_association(user)

        except():
            chair = None

    class Meta:
        verbose_name = 'Chair'
        verbose_name_plural = 'Chairs'







