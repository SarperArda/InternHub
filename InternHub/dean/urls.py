from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='dean_home'),
    path('statistics/', views.all_departments_statistics, name='dean_all_statistics'),
    path('make-announcement/', views.make_announcement, name='dean_make_announcement'),
    path('instructors/', views.instructor_list, name='dean_instructor_list'),
    path('students/', views.student_list, name='dean_student_list'),
    path('secretaries/', views.secretary_list, name='dean_secretary_list'),
]