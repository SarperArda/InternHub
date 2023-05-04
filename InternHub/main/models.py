from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin, User, Group, Permission


class Departments(models.TextChoices):
    CS = 'CS', 'Computer Engineering'
    EEE = 'EEE', 'Electrical and Electronics Engineering'
    IE = 'IE', 'Industrial Engineering'
    ME = 'ME', 'Mechanical Engineering'


class InternHubUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)


class InternHubUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    id = models.CharField(max_length=8, unique=True, primary_key=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(editable=False, default=timezone.now)

    objects = InternHubUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = [
        'id',
        'name',
    ]

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def get_full_name(self):
        return self.name

    def __str__(self):
        return self.id


class Student(InternHubUser):
    groups = models.ManyToManyField(Group, related_name='students')
    user_permissions = models.ManyToManyField(Permission, related_name='student_permissions')
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, related_name='student')

    department = models.CharField(max_length=3, choices=Departments.choices)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Chair(InternHubUser):
    groups = models.ManyToManyField(Group, related_name='chairs')
    user_permissions = models.ManyToManyField(Permission, related_name='chair_permissions')
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, related_name='chair')

    is_staff = models.BooleanField(default=True)
    department = models.CharField(max_length=3, choices=Departments.choices)

    class Meta:
        verbose_name = 'Chair'
        verbose_name_plural = 'Chairs'


class Instructor(InternHubUser):
    groups = models.ManyToManyField(Group, related_name='instructors')
    user_permissions = models.ManyToManyField(Permission, related_name='instructor_permissions')
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, related_name='instructor')

    department = models.CharField(max_length=3, choices=Departments.choices)

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'


class DepartmentSecretary(InternHubUser):
    groups = models.ManyToManyField(Group, related_name='dep_secretaries')
    user_permissions = models.ManyToManyField(Permission, related_name='dep_secretary_permissions')
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, related_name='dep_secretary')

    department = models.CharField(max_length=3, choices=Departments.choices)
    is_staff = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Department Secretary'
        verbose_name_plural = 'Department Secretaries'


class Dean(InternHubUser):
    groups = models.ManyToManyField(Group, related_name='deans')
    user_permissions = models.ManyToManyField(Permission, related_name='dean_permissions')
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, related_name='dean')

    is_staff = models.BooleanField(default=True)
    department = models.CharField(max_length=3, choices=Departments.choices)

    class Meta:
        verbose_name = 'Dean'
        verbose_name_plural = 'Deans'


class SuperUser(InternHubUser):
    groups = models.ManyToManyField(Group, related_name='superusers')
    user_permissions = models.ManyToManyField(Permission, related_name='superuser_permissions')
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, related_name='superuser')

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Superuser'
        verbose_name_plural = 'Superusers'
