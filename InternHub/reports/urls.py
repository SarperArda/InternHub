from django.urls import path
from . import views
app_name = 'reports'

urlpatterns = [
    
    path('create-confidential-form/', views.CreateConfidentialForm.as_view(), name='create_cf'),
    path('create-summer-training-form/', views.CreateSummerTrainingGradingForm.as_view(), name='create_stf'),
    path('create-work-and-report-ev-form/', views.CreateWorkAndReportEvaluationForm.as_view(), name='create_wre'),
    path('submit-report/', views.CreateSubmitReport.as_view(), name='submit_report'),
    path('submit-feedback/', views.CreateFeedback.as_view(), name='submit_feedback'),
    path('view-reports/', views.ReportsView.as_view(), name='view_reports'),
    path('main/', views.MainView.as_view(), name='main'),
]
'''
    path('create-confidential-form/<int:internship_id>', views.CreateConfidentialForm.as_view(), name='create_cf'),
    path('create-summer-training-form/<int:internship_id>', views.CreateSummerTrainingGradingForm.as_view(), name='create_stf'),
    path('create-work-and-report-ev-form/<int:internship_id>', views.CreateWorkAndReportEvaluationForm.as_view(), name='create_wre'),
    path('submit-report/<int:internship_id>', views.CreateSubmitReport.as_view(), name='submit_report'),
    path('submit-feedback/<int:internship_id>', views.CreateFeedback.as_view(), name='submit_feedback'),
    path('view-reports/<int:internship_id>', views.ReportsView.as_view(), name='view_reports'),
    path('main/<int:internship_id>', views.MainView.as_view(), name='main'),
    '''