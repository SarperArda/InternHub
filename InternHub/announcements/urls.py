from django.urls import path
from . import views
from . import forms

app_name = 'announcements'

urlpatterns = [
    path('make-announcement/', views.MakeAnnouncementView.as_view(), name='announce'),
]
