from django.contrib import admin
from .models import Internship

class InternshipAdmin(admin.ModelAdmin):
    list_display = ['student', 'instructor', 'course', 'company', 'status',]
    list_filter = ['status']
    search_fields = ['student__first_name', 'student__last_name', 'instructor__first_name', 'instructor__last_name', 'company__name']
    fields = ['student', 'instructor', 'course', 'company', 'status', 'company_approval']

admin.site.register(Internship, InternshipAdmin)
