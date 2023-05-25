from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.decorators import allowed_users
from django.utils.decorators import method_decorator
from .forms import AnnouncementForm
from users.views import RoleRequiredMixin


class MakeAnnouncementView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    login_url = '/login/'
    form_class = AnnouncementForm
    template_name = 'announcements/announcement.html'
    success_url = '/'
    allowed_roles = ['SUPERUSER', 'DEAN', 'CHAIR', 'DEPARTMENT_SECRETARY']

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.save()
        return super().form_valid(form)
