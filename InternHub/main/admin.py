from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Dean, Chair, Instructor, DepartmentSecretary, User


# Registering user models to admin.
@admin.register(User)
class DefaultAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('user_id', 'role',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_id', 'role',),
        }),
    )
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'role', 'is_staff',)
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active',)
    search_fields = ('user_id', 'email', 'first_name', 'last_name',)
    ordering = ('role', 'user_id',)


@admin.register(Student)
@admin.register(Chair)
@admin.register(Instructor)
@admin.register(DepartmentSecretary)
@admin.register(Dean)
class RoleAdmin(DefaultAdmin):
    fieldsets = (
        (None, {'fields': ('user_id',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'department',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'first_name', 'last_name', 'email', 'department', 'password1', 'password2',),
        }),
    )
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'role', 'is_staff',)
    list_filter = ('department',)
    search_fields = ('user_id', 'first_name', 'last_name', 'department',)
    ordering = ('department', 'user_id',)


# Admin panel styling
admin.site.site_title = 'InternHub'
admin.site.index_title = 'Welcome to Administration Page'
admin.site.site_header = 'InternHub Administration System'
