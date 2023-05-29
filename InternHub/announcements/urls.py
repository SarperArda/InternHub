from django.urls import path

from . import views

app_name = 'announcements'

urlpatterns = [
    path('make-announcement/', views.MakeAnnouncementView.as_view(), name='announce'),
]
