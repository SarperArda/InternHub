from django.urls import path
from . import views
from . import forms


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.HomeView.as_view(), name='home'),
]
