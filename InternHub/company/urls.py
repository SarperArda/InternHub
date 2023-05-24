from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('request-company/', views.CreateCompanyRequestView.as_view(), name='company-creation'),
    path('companies/', views.CompaniesView.as_view(), name='companies'),
    path('requests/', views.ListCompanyRequestsView.as_view(), name='company-requests'),
    path('requests/<int:pk>/', views.CompanyRequestDetailView.as_view(), name='request-detail'),
]
