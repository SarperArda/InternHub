from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='departmentSecretary_home'),
    path('company-reqests/', views.list_company_request, name='departmentSecretary_company_requests'),
    path('company-addition/', views.add_company, name='departmentSecretary_company_addition'),
    path('student-list/', views.student_list, name='departmentSecretary_student_list'),
    path('instructor-list/', views.instructor_list, name='departmentSecretary_instructor_list'),
    path('assignment/', views.assign_students_to_instructors, name='departmentSecretary_assignment'),
    path('company-approval-validation-application/', views.list_company_approval_validation_application,
         name='departmentSecretary_CAVA_list'),
    path('company-evaluation-by-student/', views.list_company_evaluation_by_student,
         name='departmentSecretary_CEBS'),
    path('company-list/', views.company_list, name="departmentSecretary_company_list"),
    path('make-announcement/', views.make_announcement, name="departmentSecretary_make_Announcement")
]