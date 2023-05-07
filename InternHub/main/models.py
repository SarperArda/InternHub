from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission


class EngineeringDepartments(models.TextChoices):
    CS = 'CS', 'Computer Engineering'
    EEE = 'EEE', 'Electrical and Electronics Engineering'
    IE = 'IE', 'Industrial Engineering'
    ME = 'ME', 'Mechanical Engineering'


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
    def create_user(self, email, user_id, password=None, first_name=None, last_name=None):
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

    def create_superuser(self, email, user_id, password=None):
        user = self.create_user(
            user_id=user_id,
            email=self.normalize_email(email),
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

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    user_permissions = models.ManyToManyField(Permission, related_name='%(class)spermissions', blank=True)

    def __str__(self):
        if self.first_name or self.last_name is None:
            return self.user_id
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Student(User):
    class Courses(models.TextChoices):
        CS299 = 'CS299', 'CS299'
        CS399 = 'CS399', 'CS399'
        EEE299 = 'EEE299', 'EEE299'
        EEE399 = 'EEE399', 'EEE399'
        ME299 = 'ME299', 'ME299'
        ME399 = 'ME399', 'ME399'
        IE299 = 'IE299', 'IE299'
        IE399 = 'IE399', 'IE399'

    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)
    course = models.CharField(max_length=6, choices=Courses.choices, blank=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Chair(User):
    is_staff = True
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Chair'
        verbose_name_plural = 'Chairs'


class Instructor(User):
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'


class DepartmentSecretary(User):
    is_staff = True
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Department Secretary'
        verbose_name_plural = 'Department Secretaries'


class Dean(User):
    is_staff = True
    department = models.CharField(max_length=3, choices=EngineeringDepartments.choices)

    class Meta:
        verbose_name = 'Dean'
        verbose_name_plural = 'Deans'


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
