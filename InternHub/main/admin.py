from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Dean, Chair, Instructor, DepartmentSecretary, User

admin.site.site_header = 'InternHub Administration System'
admin.site.index_title = 'Welcome to Administration Page'
admin.site.site_title = 'InternHub'


class DefaultAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (None, {'fields': ('user_id', 'role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_id', 'role'),
        }),
    )
    list_display = ('user_id', 'email', 'first_name',
                    'last_name', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role',)
    search_fields = ('user_id', 'email', 'first_name', 'last_name')
    ordering = ('user_id', 'email', 'first_name', 'last_name', 'role')


class RoleAdmin(DefaultAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (None, {'fields': ('user_id',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'user_id', 'first_name', 'last_name', 'email', 'password1', 'password2', 'department'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'department')


admin.site.register(User, DefaultAdmin)
admin.site.register(Student, RoleAdmin)
admin.site.register(Chair, RoleAdmin)
admin.site.register(Instructor, RoleAdmin)
admin.site.register(DepartmentSecretary, RoleAdmin)
admin.site.register(Dean, RoleAdmin)
