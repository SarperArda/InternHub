
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from announcements.models import Announcement, Notification
from reports.models import Internship


class HomeView(LoginRequiredMixin, View):
    template_name = 'main/home.html'

    def get(self, request):
        announcements = Announcement.objects.all()
        notifications = Notification.objects.filter(receiver=request.user)
        full_name = str(request.user)
        user = request.user
        id = request.user.user_id
        if(user.role != 'SUPERUSER'):
            check = True
            internship = Internship.objects.filter(student_id=id)
            return render(request, 'main/home.html', {'announcements': announcements,'notifications': notifications , 'full_name': full_name, 'user': user, 'internship': internship, 'check': check})
        return render(request, 'main/home.html', {'announcements': announcements, 'full_name': full_name})