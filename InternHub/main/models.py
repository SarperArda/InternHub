from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_student(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'student')
        return self.create_user(email, password, **extra_fields)

    def create_instructor(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'instructor')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USER_TYPES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    user_type = models.CharField(
        _('user type'), max_length=50, choices=USER_TYPES, default='student'
    )

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return False


class Student(CustomUser):
    student_id = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')


class Instructor(CustomUser):
    department = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = _('instructor')
        verbose_name_plural = _('instructors')
