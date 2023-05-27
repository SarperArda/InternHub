from django.urls import path
from . import views
app_name = 'reports'

urlpatterns = [
    path('submit-feedback/<int:pk>/', views.CreateFeedback.as_view(), name='submit_feedback'),
    path('submit-report/<int:pk>', views.CreateSubmitReport.as_view(), name='submit_report'),

    path('view-reports/', views.ReportsView.as_view(), name='view_reports'),
    path('view-internships/', views.ListInternshipsView.as_view(), name='view_internships'),
    path('internship-detail/<int:pk>/', views.InternshipDetailView.as_view(), name='internship_detail'),

    path('create-confidential-form/<int:pk>', views.CreateConfidentialForm.as_view(), name='create_cf'),
    path('create-summer-training-form/', views.CreateSummerTrainingGradingForm.as_view(), name='create_stf'),
    #path('create-work-and-report-ev-form/', views.CreateWorkAndReportEvaluationForm.as_view(), name='create_wre'),
    
    path('main/', views.MainView.as_view(), name='main'),
    path('edit-work-and-report-ev-form/<int:pk>', views.EditWorkAndReportEvaluation.as_view(), name='edit_wre'),
    path('create-work-and-report-ev-form/<int:pk>', views.WorkAndReportEvaluationFormCreation.as_view(), name='create_wre'),
    path('update-work-and-report-ev-form/<int:pk>', views.WorkAndReportEvaluationFormUpdate.as_view(), name='update_wre'),
    path('assign-internships/', views.InternshipAssignmentView.as_view(), name='assign_internships')
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