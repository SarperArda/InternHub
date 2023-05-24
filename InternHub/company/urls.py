from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('create-company/', views.CreateCompanyView.as_view(), name='company-creation'),
    path('companies/', views.CompaniesView.as_view(), name='companies'),
]
