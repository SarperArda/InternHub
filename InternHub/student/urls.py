from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='student_home'),
    path('feedbacks/', views.feedback_list, name='student_feedbacks'),
    path('submissions/', views.submission_list, name='student_submissions'),
    path('CAVA/', views.company_approval_validation_application, name='student_CAVA'),
    path('CEBS/', views.company_evaluation, name='student_company_evaluation'),
    path('profile/', views.profile, name='profile'),
    path('contacts/', views.contacts, name='contacts'),
    path('company-request/', views.company_request_application, name='student_company_request')
]