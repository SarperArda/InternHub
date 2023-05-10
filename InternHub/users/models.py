from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
# Create your models here.


class EngineeringDepartment(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Course.objects.create(code=self.code + "299", name="Summer Training 1")
        Course.objects.create(code=self.code + "399", name="Summer Training 2")


class Course(models.Model):
    code = models.CharField(max_length=6, unique=True)
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
        if self.first_name or self.last_name is None:
            return self.user_id
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Instructor(User):

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'


class Student(User):
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, related_name='students')
    assigned_instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, related_name='students')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Chair(User):
    is_staff = True

    class Meta:
        verbose_name = 'Chair'
        verbose_name_plural = 'Chairs'


class DepartmentSecretary(User):
    is_staff = True

    class Meta:
        verbose_name = 'Department Secretary'
        verbose_name_plural = 'Department Secretaries'


class Dean(User):
    is_staff = True

    class Meta:
        verbose_name = 'Dean'
        verbose_name_plural = 'Deans'
