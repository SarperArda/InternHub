from django.urls import path
from . import views
app_name = 'reports'

urlpatterns = [
    path('create-confidential-form/<int:internship_id>', views.CreateConfidentialForm.as_view(), name='create_cf'),
    path('create-summer-training-form/<int:internship_id>', views.CreateSummerTrainingGradingForm.as_view(), name='create_stf'),
    path('create-work-and-report-ev-form/<int:internship_id>', views.CreateWorkAndReportEvaluationForm.as_view(), name='create_wre'),
    path('submit-report/', views.CreateSubmitReport.as_view(), name='create_report'),
]
