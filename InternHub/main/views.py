from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from announcements.models import Announcement
from reports.models import Internship
from users.models import DepartmentSecretary, Chair, Dean


class HomeView(LoginRequiredMixin, View):
    template_name = 'main/home.html'

    def get(self, request):
        announcements = Announcement.objects.all()
        full_name = str(request.user)
        user = request.user
        id = request.user.user_id
        contacts_tuple = (DepartmentSecretary.objects.all().filter(department=user.department),
                          Chair.objects.all().filter(department=user.department),
                          Dean.objects.all().filter(department=user.department),)
        if user.role != 'SUPERUSER':
            check = True
            internship = Internship.objects.filter(student__user_id=id)[0]
            if user.role == 'STUDENT':
                contacts_tuple += ((internship.instructor,),)
            return render(request, 'main/home.html',
                          {'announcements': announcements, 'full_name': full_name, 'user': user,
                           'internship': internship, 'check': check, 'contacts_tuple': contacts_tuple})
        return render(request, 'main/home.html', {'announcements': announcements, 'full_name': full_name})
