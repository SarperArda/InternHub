from django.urls import path
from . import views
app_name = 'reports'

urlpatterns = [
    path('create-confidential-form/', views.CreateConfidentialForm.as_view(), name='login'),
]
