from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from announcements.models import Announcement, Notification
from reports.models import Internship, Statistic
from users.models import DepartmentSecretary, Chair, Dean
from django.utils import timezone


class HomeView(LoginRequiredMixin, View):
    template_name = 'main/home.html'

    def get(self, request):
        announcements = Announcement.objects.all().order_by('-id')
        notifications = Notification.objects.filter(receiver=request.user).order_by('-id')
        full_name = str(request.user)
        user = request.user
        id = request.user.user_id
        contacts_set: set = {DepartmentSecretary.objects.all().filter(department=user.department),
                             Chair.objects.all().filter(department=user.department),
                             Dean.objects.all().filter(department=user.department), }
        if user.role != 'SUPERUSER':
            check = True
            internships = Internship.objects.filter(student__user_id=id)
            csPk = None
            mePk = None
            eePk = None
            iePk = None
            statistics = None
            due_date = None
            if user.role == 'STUDENT':
                for internship in internships:
                    contacts_set.add((internship.instructor,))
                    if internship.submissions.exists():
                        last_submission = internship.submissions.last()               
                        if (last_submission.status == 'PE' and last_submission.due_date > timezone.now()):
                            if due_date is None or last_submission.due_date > due_date:
                                due_date = last_submission.due_date

            if user.role == 'DEAN':
                csPk = Statistic.objects.all()[0].pk
                mePk = Statistic.objects.all()[1].pk
                eePk = Statistic.objects.all()[2].pk
                iePk = Statistic.objects.all()[3].pk
            if user.role == 'CHAIR':
                statistics = Statistic.objects.filter(department=user.department).first().pk
            return render(request, 'main/home.html',
                          {'announcements': announcements, 'full_name': full_name, 'user': user,
                           'internships': internships, 'check': check, 'contacts_set': contacts_set,
                             'notifications': notifications, 'statistics': statistics, 'csPk': csPk, 'mePk': mePk, 'eePk': eePk, 'iePk': iePk, 'due_date': due_date})  
        return render(request, 'main/home.html', {'user': user, 'announcements': announcements, 'notifications': notifications, 'full_name': full_name})