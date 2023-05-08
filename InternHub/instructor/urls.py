from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='instructor_home'),
    path('give-feedback/', views.give_feedback, name='instructor_give_feed_back'),
    path('students/', views.student_list, name='instructor_student_list'),
    path('feedbacks/', views.feedback_list, name='instructor_feedback_list'),
    path('stgf-list/', views.summer_training_grading_form_list, name='instructor-stgf'),
    path('stwef-list/', views.summer_training_work_evaluation_form_list, name='instructor-stwef'),
    path('create-stgf/', views.create_summer_training_grading_form, name='instructor_create_stgf'),
    path('create-stwef/', views.create_summer_training_work_evaluation, name='instructor_create_stwef'),
    path('open-submission/', views.open_submission, name='instructor_open_submission'),
    path('edit-stgf/', views.edit_summer_training_grading_form, name='instructor_edit_stgf'),
    path('edit-stwef/', views.edit_summer_training_work_evaluation, name='instructor_edit_stwef'),
]