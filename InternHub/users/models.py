import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
from django.db import models

from .decorators import decorate_get_all


# Create your models here.


class EngineeringDepartment(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Course(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.code


class RoleMixin(models.Model):
    class Role(models.TextChoices):
        SUPERUSER = 'SUPERUSER', 'Superuser'
        STUDENT = 'STUDENT', 'Student'
        DEAN = 'DEAN', 'Dean'
        CHAIR = 'CHAIR', 'Chair'
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        DEPARTMENTSECRETARY = 'DEPARTMENT_SECRETARY', 'Department Secretary'

    role = models.CharField(max_length=50, choices=Role.choices, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        role = self.__class__.__name__.upper()
        if role == 'USER':
            self.role = self.Role.SUPERUSER
        else:
            self.role = self.Role[role]
        super().save(*args, **kwargs)


class UserManager(BaseUserManager):

    def create_user(self, user_id, password=None, email=None, first_name=None, last_name=None):
        if not user_id:
            raise ValueError('Users must have a valid id')

        user = self.model(
            user_id=user_id,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None):
        user = self.create_user(
            user_id=user_id,
            password=password,
        )

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.role = RoleMixin.Role.SUPERUSER
        user.save(using=self._db)
        return user

    @staticmethod
    def create_instructors():
        with open('fixtures/instructors.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = UserManager.determine_pk(user['fields']['department'])
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                instructor = Instructor(**user['fields'], password=hashed_password)
                instructor.save()

    @staticmethod
    def create_students():
        with open('fixtures/students.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = UserManager.determine_pk(user['fields']['department'])
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                student = Student(**user['fields'], password=hashed_password)
                student.save()

    @staticmethod
    def create_department_secretaries():
        with open('fixtures/secretary.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = UserManager.determine_pk(user['fields']['department'])
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                ds = DepartmentSecretary(**user['fields'], password=hashed_password)
                ds.save()

    @staticmethod
    def create_dean():
        with open('fixtures/dean.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = UserManager.determine_pk(user['fields']['department'])
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                dean = Dean(**user['fields'], password=hashed_password)
                dean.save()

    @staticmethod
    def create_chairs():
        with open('fixtures/chairs.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = UserManager.determine_pk(user['fields']['department'])
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                chair = Chair(**user['fields'], password=hashed_password)
                chair.save()

    @staticmethod
    def create_supers():
        with open('fixtures/superuser.json') as file:
            data = json.load(file)
            hashed_password = make_password('admin')
            for user in data:
                department_id = UserManager.determine_pk(user['fields']['department'])
                department = EngineeringDepartment.objects.get(pk=department_id)
                user['fields']['department'] = department
                super_user = User(**user['fields'], password=hashed_password)
                super_user.role = RoleMixin.Role.SUPERUSER
                super_user.save()

    @staticmethod
    def create_users():
        UserManager.create_instructors()
        UserManager.create_dean()
        UserManager.create_students()
        UserManager.create_department_secretaries()
        UserManager.create_supers()
        UserManager.create_chairs()

    @staticmethod
    def determine_pk(pk):
        cs_pk = EngineeringDepartment.objects.all()[0].pk
        me_pk = EngineeringDepartment.objects.all()[1].pk
        eee_pk = EngineeringDepartment.objects.all()[2].pk
        ie_pk = EngineeringDepartment.objects.all()[3].pk
        if pk == 1:
            return cs_pk
        elif pk == 2:
            return me_pk
        elif pk == 3:
            return eee_pk
        else:
            return ie_pk


# Your existing code here

class User(AbstractBaseUser, PermissionsMixin, RoleMixin):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    email = models.EmailField(max_length=50, unique=True, null=True)
    user_id = models.CharField(max_length=8, unique=True, null=False)
    department = models.ForeignKey(
        EngineeringDepartment, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    user_permissions = models.ManyToManyField(
        Permission, related_name='%(class)spermissions', blank=True)

    def __str__(self):
        if self.first_name is None or self.last_name is None:
            return self.user_id
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Instructor(User):
    is_staff = True

    def assign_students_to_instructor(self, student):
        self.students.add(student)

    def remove_students_to_instructor(self, student):
        self.students.remove(student)

    def update_instructor_association(self, is_add, student):
        if is_add:
            self.assign_students_to_instructor(student)
        else:
            self.students.remove(student)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'


class Student(User):
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class DepartmentSecretary(User):
    is_staff = True

    def get_students_of_secretary(self):
        return Student.objects.all().filter(department=self.department)

    def get_instructors_of_secretary(self):
        return Instructor.objects.all().filter(department=self)

    @staticmethod
    def get_secretary_of_department(department):
        return DepartmentSecretary.objects.get(department=department)

    @staticmethod
    def assign_tos(instructor, student):
        if student.grading_instructor is None:
            instructor.assign_students_to_instructor(student)
        else:
            student.grading_instructor.remove_students_to_instructor(student)
            instructor.assign_students_to_instructor(student)

    class Meta:
        verbose_name = 'Department Secretary'
        verbose_name_plural = 'Department Secretaries'


class Chair(User):
    is_staff = True

    def get_students_of_chair(self):
        return Student.objects.all().filter(department=self.department)

    def get_instructors_of_chair(self):
        return Instructor.objects.all().filter(department=self.department)

    def get_secretary_of_chair(self):
        return DepartmentSecretary.objects.get(department=self.department)

    @staticmethod
    def get_chair_of_department(department):
        return Chair.objects.get(department=department)

    class Meta:
        verbose_name = 'Chair'
        verbose_name_plural = 'Chairs'


class Dean(User):
    is_staff = True

    @staticmethod
    def get_dean():
        return Dean.objects.all().first()

    @staticmethod
    @decorate_get_all(Chair)
    def get_all_chairs():
        pass

    @staticmethod
    @decorate_get_all(Student)
    def get_all_students():
        pass

    @staticmethod
    @decorate_get_all(Instructor)
    def get_all_instructors():
        pass

    @staticmethod
    @decorate_get_all(DepartmentSecretary)
    def get_all_secretaries():
        pass

    class Meta:
        verbose_name = 'Dean'
        verbose_name_plural = 'Deans'
