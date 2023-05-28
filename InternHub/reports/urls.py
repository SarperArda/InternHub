from django.urls import path
from . import views
app_name = 'reports'

urlpatterns = [
    path('view-reports/', views.ReportsView.as_view(), name='view_reports'),
    path('view-internships/', views.ListInternshipsView.as_view(), name='view_internships'),
    path('internship-detail/<int:pk>/', views.InternshipDetailView.as_view(), name='internship_detail'),

    path('create-confidential-form/<int:pk>', views.CreateConfidentialForm.as_view(), name='create_cf'),
    
    path('edit-work-and-report-ev-form/<int:pk>', views.EditWorkAndReportEvaluation.as_view(), name='edit_wre'),
    path('create-work-and-report-ev-form/<int:pk>', views.WorkAndReportEvaluationFormCreation.as_view(), name='create_wre'),
    path('update-work-and-report-ev-form/<int:pk>', views.WorkAndReportEvaluationFormUpdate.as_view(), name='update_wre'),
    path('assign-internships/', views.InternshipAssignmentView.as_view(), name='assign_internships'),

    path('submissions/', views.ListSubmissionView.as_view(), name='submission_list'),
    path('feedbacks/', views.ListFeedbackView.as_view(), name='feedback_list'),
    path('statistics/<int:pk>', views.StatisticView.as_view(), name='statistics'),
]
