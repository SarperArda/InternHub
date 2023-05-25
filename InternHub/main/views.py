
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from announcements.models import Announcement


class HomeView(LoginRequiredMixin, View):
    template_name = 'main/home.html'

    def get(self, request):
        announcements = Announcement.objects.all()
        full_name = str(request.user)
        return render(request, 'main/home.html', {'announcements': announcements, 'full_name': full_name})