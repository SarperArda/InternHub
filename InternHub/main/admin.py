from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Dean, Chair, Instructor, DepartmentSecretary, SuperUser, User

admin.site.site_header = 'InternHub Administration System'
admin.site.index_title = 'Welcome to Administration Page'
admin.site.site_title = 'InternHub'


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ('id', 'email', 'name', 'department',)
    list_filter = ('department',)
    search_fields = ('id', 'name',)
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('id', 'password',)}),
        ('Personal info', {'fields': ('email', 'name', 'department',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email', 'name', 'department',
                       'password1', 'password2',)}
         ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.name = form.cleaned_data['name']
            obj.email = form.cleaned_data['email']
            obj.id = form.cleaned_data['id']
            obj.department = form.cleaned_data['department']
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)


@admin.register(Dean)
@admin.register(Chair)
@admin.register(Instructor)
@admin.register(DepartmentSecretary)
class StaffAdmin(UserAdmin):
    list_display = ('id', 'email', 'name', 'department', 'is_staff',)
    list_filter = ('department',)
    search_fields = ('id', 'name',)
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('id', 'password')}),
        ('Personal info', {'fields': ('email', 'name', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email', 'name', 'department',
                       'password1', 'password2', 'is_staff',)}
         ),
    )


@admin.register(SuperUser)
class SuperUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'name', 'is_staff', 'is_superuser',)
    list_filter = ()
    search_fields = ('id', 'name',)
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('id', 'password',)}),
        ('Personal info', {'fields': ('email', 'name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email', 'name', 'password1',
                       'password2', 'is_staff', 'is_superuser',)}
         ),
    )
