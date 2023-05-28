from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('companies/', views.CompaniesView.as_view(), name='companies'),

    path('request-company/', views.CreateCompanyRequestView.as_view(), name='company-creation'),
    path('company-requests/', views.ListCompanyRequestsView.as_view(), name='company-requests'),
    path('company-requests/<int:pk>/', views.CompanyRequestDetailView.as_view(), name='request-detail'),

    path('request-cava/', views.CreateCAVAView.as_view(), name="cava-creation"),
    path('cava-requests/', views.ListCAVASView.as_view(), name="cava-requests"),
    path('cava-requests/<int:pk>/', views.CAVADetailView.as_view(), name="cava-detail"),

    path('company-evaluation/<int:pk>/', views.CompanyEvaluationView.as_view(), name="evaluate-company"),
    path('company-evaluation/', views.ListCompanyEvaluationsView.as_view(), name="company-evaluations"),
]