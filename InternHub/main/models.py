from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User, Group, Permission


class EngineeringDepartments(models.TextChoices):
    CS = 'CS', 'Computer Engineering'
    EEE = 'EEE', 'Electrical and Electronics Engineering'
    IE = 'IE', 'Industrial Engineering'
    ME = 'ME', 'Mechanical Engineering'


class InternHubUserManager(BaseUserManager):
    def create_user(self, bilkent_id, password=None, **kwargs):
        if not bilkent_id:
            raise ValueError('Users must have a valid bilkent id')

        new_user = self.model(bilkent_id=bilkent_id, **kwargs)
        new_user.set_password(password)

        user_model = get_user_model()
        user = user_model.objects.create_user(username=bilkent_id, password=password)
        user.name = new_user.name
        user.email = new_user.email
        user.is_active = new_user.is_active
        user.is_staff = new_user.is_staff
        user.is_superuser = new_user.is_superuser
        user.save()

        new_user.user = user
        new_user.save(using=self._db)
        return new_user

    def create_superuser(self, bilkent_id, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(bilkent_id, password, **kwargs)


class InternHubUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        abstract = True

    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True)
    bilkent_id = models.CharField(max_length=8, primary_key=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(editable=False, default=timezone.now)

    groups = models.ManyToManyField(Group, related_name='%(class)s')
    user_permissions = models.ManyToManyField(Permission, related_name='%(class)_permissions')

    objects = InternHubUserManager()

    USERNAME_FIELD = 'bilkent_id'
    REQUIRED_FIELDS = [
        'bilkent_id',
    ]

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.bilkent_id}: {self.name}'


class Student(InternHubUser):
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Chair(InternHubUser):
    is_staff = models.BooleanField(default=True)
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Chair'
        verbose_name_plural = 'Chairs'


class Instructor(InternHubUser):
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'


class DepartmentSecretary(InternHubUser):
    is_staff = models.BooleanField(default=True)
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Department Secretary'
        verbose_name_plural = 'Department Secretaries'


class Dean(InternHubUser):
    is_staff = models.BooleanField(default=True)
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Dean'
        verbose_name_plural = 'Deans'


class SuperUser(InternHubUser):
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Superuser'
        verbose_name_plural = 'Superusers'
