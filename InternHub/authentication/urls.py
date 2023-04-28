from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),
    path('logout/', views.logout_page, name='logout'),
]
