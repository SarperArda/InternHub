from django.urls import path
from . import views
from . import forms

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
