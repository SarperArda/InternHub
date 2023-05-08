from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='chair_home'),
    path('statistics/', views.department_statistics, name='chair_statistics'),
    path('make-announcement/', views.make_announcement, name='chair_make_announcement'),
    path('instructors/', views.instructor_list, name='chair_instructor_list'),
    path('students/', views.student_list, name='chair_student_list'),
]

