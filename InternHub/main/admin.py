from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from student.models import Student
from dean.models import Dean
from chair.models import Chair
from instructor.models import Instructor
from departmentSecretary.models import DepartmentSecretary
from .models import User


# Registering user models to admin
@admin.register(User)
class DefaultAdmin(UserAdmin):
    """Custom admin model for built-in User model."""

    fieldsets = (
        (None, {'fields': ('user_id', 'first_name', 'last_name', 'role',)}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2',),
        }),
    )

    list_display = ('user_id', 'role', 'first_name', 'last_name', 'is_staff',)
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active',)
    search_fields = ('user_id', 'first_name', 'last_name', 'role',)
    ordering = ('role', 'user_id',)


@admin.register(Dean)
@admin.register(Chair)
@admin.register(Instructor)
@admin.register(DepartmentSecretary)
class RoleAdmin(DefaultAdmin):
    """Custom admin models for Dean, Chair, Instructor, and DepartmentSecretary."""

    def full_name(self, obj):
        return f"{obj.first_name} {str(obj.last_name).upper()}"

    full_name.short_description = 'Name'

    fieldsets = (
        (None, {'fields': ('user_id', 'first_name', 'last_name',)}),
        ('Personal info', {'fields': ('email', 'department',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'first_name', 'last_name', 'email', 'department', 'password1', 'password2',),
        }),
    )

    list_display = ('full_name', 'user_id', 'department', 'role',)
    list_filter = ('department',)
    search_fields = ('user_id', 'first_name', 'last_name', 'department',)
    ordering = ('department', 'user_id',)


@admin.register(Student)
class StudentAdmin(RoleAdmin):
    """Custom admin model for Student."""

    fieldsets = (
        (None, {'fields': ('user_id', 'first_name', 'last_name',)}),
        ('Personal info', {'fields': ('email', 'department', 'course',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'first_name', 'last_name', 'email',
                       'department', 'course', 'password1', 'password2',),
        }),
    )

    list_display = ('user_id', 'first_name', 'last_name', 'department', 'course',)
    list_filter = ('department', 'course',)
    search_fields = ('user_id', 'first_name', 'last_name', 'department', 'course',)
    ordering = ('department', 'course', 'user_id',)


# Admin panel styling
admin.site.site_title = 'InternHub'
admin.site.index_title = 'Welcome to Administration Page'
admin.site.site_header = 'InternHub Administration System'
